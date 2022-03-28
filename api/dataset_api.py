from flask_restful import Api, Resource, reqparse
from flask import send_file
import pymongo
from math import ceil
import json
from api.detection_code.scraper.metadata_scraper import getInfo
from api.detection_code.scraper.caption_scraper import captionScraper
import requests


class DatasetGetterAPIHandler(Resource):
    def hash(self, val_name):
        return val_name['value'] + "/--/" + val_name['name']

    def unhash(self, val_name):
        return {
            "value": val_name.split('/--/')[0],
            "name": val_name.split('/--/')[1]
        }

    def get(self):
        db = pymongo.MongoClient('localhost:27017')['YT_Misinfo_Dataset']
        vids = list(db['Video_Dataset'].find({}, {'_id': 0, 'Topic': 1, 'tags': 1}))
        topics_set = set()
        for v in vids:
            if 'Topic' in v.keys():
                topics_set.add(self.hash(v['Topic']))
        topics_set = sorted(topics_set)
        topics = []
        for t in topics_set:
            topics.append(self.unhash(t))
        tags_set = set()
        for v in vids:
            # print(v)
            for t in v['tags']:
                tags_set.add(t)
        tags = list(tags_set)
        tags = sorted(tags)
        return {
            'resultStatus': 'SUCCESS',
            'topics': topics,
            'tags': tags
        }
        # [
        #     {
        #         "name": "9/11 Conspiracy Theory",
        #         "value": "911"
        #     },
        #     {
        #         "name": "Chemtrails Conspiracy Theory",
        #         "value": "chemtrails"
        #     },
        #     {
        #         "name": "Flat Earth Theory",
        #         "value": "flatearth"
        #     },
        #     {
        #         "name": "Moonlanding",
        #         "value": "moonlanding"
        #     },
        #     {
        #         "name": "Vaccine Controversy",
        #         "value": "vaccines"
        #     },
        # ]

    def post(self):
        parser = reqparse.RequestParser()
        # parser.add_argument('type', type=str)
        parser.add_argument('page', type=int)
        parser.add_argument('topicFilter', type=list)

        args = parser.parse_args()

        print(args)
        if len(args['topicFilter']) == 0:
            return {
                "status": "Success",
                "num_pages": 0,
                "videoList": [],
            }
        db = pymongo.MongoClient('localhost:27017')['YT_Misinfo_Dataset']
        filter = []
        for t in args['topicFilter']:
            # filter.append({
            #     "Topic.value": t
            # })
            filter.append({
                "tags": t
            })
        print(filter)
        vids = list(db['Video_Dataset'].find({
            "$or": filter
        }, {'_id': 0})[(args['page']-1)*10:args['page']*10])
        print(len(vids))
        # note, the post req from frontend needs to match the strings here (e.g. 'type and 'message')
        # for i in args['topicFilter']:
        #     print(i)

        # final_ret = {"status": "Success", "message": message}
        # print(final_ret)
        return {
            "status": "Success",
            "num_pages": ceil(db['Video_Dataset'].count_documents({
                "$or": filter
            })/10),
            "videoList": vids,
        }


class DatasetUpdaterAPIHandler(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str)

        args = parser.parse_args()

        pattern = '"playabilityStatus":{"status":"ERROR","reason":"Video unavailable"'
        request = requests.get(args['url'])
        if pattern in request.text:
            return {"valid": False}

        try:
            Video_ID = args['url'].split('v=')[1].split('&')[0]
            db = pymongo.MongoClient('localhost:27017')['YT_Misinfo_Dataset']
            return {"valid": db['Video_Dataset'].find_one({"Video_ID": Video_ID}) is None}
        except:
            return {"valid": False}

    def post(self):
        parser = reqparse.RequestParser()
        # parser.add_argument('type', type=str)
        parser.add_argument('url', type=str)
        parser.add_argument('suggestedLabel', type=int)
        parser.add_argument('reason', type=str)
        parser.add_argument('tags', type=list)

        args = parser.parse_args()

        print(args)
        args['tags'] = list(set(args['tags']))
        # Check if url already present.
        db = pymongo.MongoClient('localhost:27017')['YT_Misinfo_Dataset']
        existing_vid = db['Video_Dataset'].find_one({
            "vid_url": args['url']
        }, {'_id': 0, 'tags': 1})
        print(existing_vid)
        if not existing_vid:
            # If no, then scrape the data using scraper, then add to voting poll.
            vid_info = getInfo(args['url'])
            if not vid_info:
                return {
                    "status": "Failed",
                    "reason": "Video url not valid."
                }
            Video_ID = args['url'].split('v=')[1].split('&')[0]
            vid_info['Video_ID'] = Video_ID
            captions = captionScraper(Video_ID)
            if captions is not None:
                vid_info['Captions'] = captions
            else:
                return {
                    "status": "Failed",
                    "reason": "Video does not have English subtitles."
                }
            vid_info['tags'] = args['tags']
            print(vid_info)
            
            db['Video_Dataset'].find_one_and_update(
                {
                    "vid_url": args['url']
                },
                {
                    "$set": vid_info
                },
                upsert = True
            )
        else:
            newTags = set()
            for t in args['tags']:
                newTags.add(t)
            for t in existing_vid['tags']:
                newTags.add(t)
            newTags = list(newTags)
            db['Video_Dataset'].find_one_and_update(
                {
                    "vid_url": args['url']
                },
                {
                    "$set": {
                        "tags": newTags
                    }
                }
            )

        # If yes/newly added, then add to voting poll.
        existing_vid = db['Video_Dataset'].find_one({
            "vid_url": args['url'],
            "voting.{}.reason".format(args['suggestedLabel']): args['reason']
        }, {'_id': 0})
        if existing_vid:
            db['Video_Dataset'].find_one_and_update(
                {
                    "vid_url": args['url'],
                    "voting.{}.reason".format(args['suggestedLabel']): args['reason']
                },
                {
                    "$inc": {
                        "voting.{}.$.count".format(args['suggestedLabel']): 1
                    }
                }
            )
        else:
            db['Video_Dataset'].find_one_and_update(
                {
                    "vid_url": args['url']
                },
                {
                    "$push": {
                        "voting.{}".format(args['suggestedLabel']): {
                            "count": 1,
                            "reason": args['reason']
                        }
                    }
                }
            )
        
        return {
            "status": "Success",
        }


class DatasetExtractAPIHandler(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        # parser.add_argument('type', type=str)
        parser.add_argument('topicFilter', type=list)

        args = parser.parse_args()

        print(args)

        db = pymongo.MongoClient('localhost:27017')['YT_Misinfo_Dataset']
        filter = []
        for t in args['topicFilter']:
            # filter.append({
            #     "Topic.value": t
            # })
            filter.append({
                "tags": t
            })
        print(filter)
        vids = list(db['Video_Dataset'].find({
            "$or": filter
        }, {'_id': 0}))

        return json.dumps(vids)

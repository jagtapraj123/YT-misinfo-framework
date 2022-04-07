from flask_restful import Api, Resource, reqparse
from flask import send_file
import pymongo
from math import ceil
import json
from api.detection_code.scraper.metadata_scraper import getInfo
from api.detection_code.scraper.caption_scraper import captionScraper
import requests
from urllib.parse import urlparse, unquote

class DatasetGetterAPIHandler(Resource):
    # def hash(self, val_name):
    #     return val_name['value'] + "/--/" + val_name['name']

    # def unhash(self, val_name):
    #     return {
    #         "value": val_name.split('/--/')[0],
    #         "name": val_name.split('/--/')[1]
    #     }

    # def get(self):
    #     db = pymongo.MongoClient('localhost:27017')['YT_Misinfo_Dataset']
    #     # vids = list(db['Video_Dataset'].find({}, {'_id': 0, 'Topic': 1, 'tags': 1}))
    #     # topics_set = set()
    #     # for v in vids:
    #     #     if 'Topic' in v.keys():
    #     #         topics_set.add(self.hash(v['Topic']))
    #     # topics_set = sorted(topics_set)
    #     # topics = []
    #     # for t in topics_set:
    #     #     topics.append(self.unhash(t))
    #     # tags_set = set()
    #     # for v in vids:
    #     #     # print(v)
    #     #     for t in v['tags']:
    #     #         tags_set.add(t)
    #     # tags = list(tags_set)
    #     # tags = sorted(tags)

    #     mapping_list = list(db['Topics_Mapping'].find({}, {'_id': 0, 'topics': 1, 'tag': 1}))
    #     print(mapping_list)
    #     tags = set()
    #     topics = dict()
    #     for m in mapping_list:
    #         tags.add(m['tag'])
    #         if 'topics' in m.keys():
    #             for t in m['topics']:
    #                 topics[t] = topics.get(t, [])
    #                 topics[t].append(m['tag'])
    #     tags = list(tags)
    #     tags = sorted(tags)
    #     # topics = list(topics)
    #     return {
    #         'resultStatus': 'SUCCESS',
    #         'topics': topics,
    #         'tags': tags
    #     }
    #     # [
    #     #     {
    #     #         "name": "9/11 Conspiracy Theory",
    #     #         "value": "911"
    #     #     },
    #     #     {
    #     #         "name": "Chemtrails Conspiracy Theory",
    #     #         "value": "chemtrails"
    #     #     },
    #     #     {
    #     #         "name": "Flat Earth Theory",
    #     #         "value": "flatearth"
    #     #     },
    #     #     {
    #     #         "name": "Moonlanding",
    #     #         "value": "moonlanding"
    #     #     },
    #     #     {
    #     #         "name": "Vaccine Controversy",
    #     #         "value": "vaccines"
    #     #     },
    #     # ]

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

class DatasetTopicsAPIHandler(Resource):
    def get(self):
        db = pymongo.MongoClient('localhost:27017')['YT_Misinfo_Dataset']
        # vids = list(db['Video_Dataset'].find({}, {'_id': 0, 'Topic': 1, 'tags': 1}))
        # topics_set = set()
        # for v in vids:
        #     if 'Topic' in v.keys():
        #         topics_set.add(self.hash(v['Topic']))
        # topics_set = sorted(topics_set)
        # topics = []
        # for t in topics_set:
        #     topics.append(self.unhash(t))
        # tags_set = set()
        # for v in vids:
        #     # print(v)
        #     for t in v['tags']:
        #         tags_set.add(t)
        # tags = list(tags_set)
        # tags = sorted(tags)

        mapping_list = list(db['Topics_Mapping'].find({}, {'_id': 0, 'topics': 1, 'tag': 1}))
        print(mapping_list)
        tags = set()
        topics = dict()
        for m in mapping_list:
            tags.add(m['tag'])
            if 'topics' in m.keys():
                for t in m['topics']:
                    topics[t] = topics.get(t, [])
                    topics[t].append(m['tag'])
        tags = list(tags)
        tags = sorted(tags)
        # topics = list(topics)
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

class DatasetUpdaterAPIHandler(Resource):
    # def get(self):
    #     parser = reqparse.RequestParser()
    #     parser.add_argument('url', type=str)

    #     args = parser.parse_args()
    #     args['url'] = unquote(args['url'])

    #     pattern = '"playabilityStatus":{"status":"ERROR","reason":"Video unavailable"'
    #     try:
    #         request = requests.get(args['url'])
    #         if pattern in request.text:
    #             return {"valid": False}
    #     except:
    #         return {"valid": False}

    #     try:
    #         website = urlparse(args['url']).netloc
    #         website = website.lower().split('.')
    #         print(website)
    #         if "youtube" not in website:
    #             return {"valid": False}
    #         Video_ID = args['url'].split('v=')[1].split('&')[0]
    #         print(Video_ID)
    #         db = pymongo.MongoClient('localhost:27017')['YT_Misinfo_Dataset']
    #         return {"valid": db['Video_Dataset'].find_one({"Video_ID": Video_ID}) is None}
    #     except:
    #         return {"valid": False}

    def post(self):
        parser = reqparse.RequestParser()
        # parser.add_argument('type', type=str)
        parser.add_argument('url', type=str)
        parser.add_argument('suggestedLabel', type=int)
        parser.add_argument('reasons', type=list)
        parser.add_argument('tags', type=list)

        args = parser.parse_args()

        print(args)
        args['tags'] = list(set(args['tags']))
        print(args['tags'])
        # Check if url already present.
        url = args['url']
        db = pymongo.MongoClient('localhost:27017')['YT_Misinfo_Dataset']
        existing_vid = db['Video_Dataset'].find_one({
            "vid_url": url
        }, {'_id': 0, 'tags': 1})
        print(existing_vid)
        if not existing_vid:
            # If no, then scrape the data using scraper, then add to voting poll.
            vid_info = getInfo(url)
            url = vid_info['vid_url']
            print(vid_info)
            if not vid_info:
                return {
                    "status": "Failed",
                    "reason": "Video url not valid."
                }
            Video_ID = url.split('v=')[1].split('&')[0]
            vid_info['Video_ID'] = Video_ID
            existing_vid = db['Video_Dataset'].find_one({
                "Video_ID": vid_info['Video_ID']
            }, {'_id': 0, 'tags': 1})
            if existing_vid is not None:
                return {
                    "status": "Failed",
                    "reason": "Video already present in dataset."
                }
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
                    "vid_url": url
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
                    "vid_url": url
                },
                {
                    "$set": {
                        "tags": newTags
                    }
                }
            )

        # If yes/newly added, then add to voting poll.
        for r in args['reasons']:
            existing_vid = db['Video_Dataset'].find_one({
                "vid_url": url,
                "voting.{}.reason".format(args['suggestedLabel']): r
            }, {'_id': 0})
            if existing_vid:
                db['Video_Dataset'].find_one_and_update(
                    {
                        "vid_url": url,
                        "voting.{}.reason".format(args['suggestedLabel']): r
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
                        "vid_url": url
                    },
                    {
                        "$push": {
                            "voting.{}".format(args['suggestedLabel']): {
                                "count": 1,
                                "reason": r
                            }
                        }
                    }
                )
        
        mapping_list = list(db['Topics_Mapping'].find({}, {'_id': 0, 'tag': 1}))
        existing_tags = set()
        for m in mapping_list:
            existing_tags.add(m['tag'])
        for t in args['tags']:
            if t not in existing_tags:
                db['Topics_Mapping'].find_one_and_update(
                    {
                        "tag": t
                    },
                    {
                        "$set": { "topics": [] }
                    },
                    upsert=True
                )

        return {
            "status": "Success",
        }

class BasicVideoCheckingAPIHandler(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str)

        args = parser.parse_args()
        args['url'] = unquote(args['url'])
        url = args['url']

        pattern = '"playabilityStatus":{"status":"ERROR","reason":"Video unavailable"'
        try:
            request = requests.get(url)
            url = request.url
            if request.status_code != 200 or pattern in request.text:
                return {"valid": False, "reason": "URL is not a valid YouTube video."}
        except:
            return {"valid": False, "reason": "Error parsing URL. Check if valid URL is entered."}

        try:
            website = urlparse(url).netloc
            website = website.lower().split('.')
            print(website)
            if "youtube" not in website:
                return {"valid": False, "reason": "URL is not a YouTube URL."}
            Video_ID = url.split('v=')[1].split('&')[0]
            print(Video_ID)
            db = pymongo.MongoClient('localhost:27017')['YT_Misinfo_Dataset']
            if db['Video_Dataset'].find_one({"Video_ID": Video_ID}) is None:
                return {"valid": True}
            else:
                return {"valid": False, "reason": "Video already present in dataset."}
        except:
            return {"valid": False, "reason": "Error parsing URL. Check if valid URL is entered."}

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

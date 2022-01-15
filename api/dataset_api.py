from flask_restful import Api, Resource, reqparse
from flask import send_file
import pymongo
from math import ceil
import json


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
        vid_topics = list(db['video_dataset'].find({}, {'_id': 0, 'Topic': 1}))
        topics_set = set()
        for vt in vid_topics:
            topics_set.add(self.hash(vt['Topic']))
        topics_set = sorted(topics_set)
        topics = []
        for t in topics_set:
            topics.append(self.unhash(t))

        return {
            'resultStatus': 'SUCCESS',
            'topics': topics
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
            filter.append({
                "Topic.value": t
            })
        print(filter)
        vids = list(db['video_dataset'].find({
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
            "num_pages": ceil(db['video_dataset'].count_documents({
                "$or": filter
            })/10),
            "videoList": vids,
        }


class DatasetUpdaterAPIHandler(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        # parser.add_argument('type', type=str)
        parser.add_argument('url', type=str)
        parser.add_argument('suggestedLabel', type=int)
        parser.add_argument('reason', type=str)

        args = parser.parse_args()

        print(args)
        # Check if url already present.
        db = pymongo.MongoClient('localhost:27017')['YT_Misinfo_Dataset']
        existing_vid = db['video_dataset'].find_one({
            "vid_url": args['url']
        }, {'_id': 0})
        print(existing_vid)
        if existing_vid:
            # If yes, then add to voting poll.
            db['video_dataset'].find_one_and_update(
                {
                    "vid_url": args['url']
                },
                {
                    "$push": {
                        "voting": {
                            "suggested_label": args['suggestedLabel'],
                            "reason": args['reason']
                        }
                    }
                }
            )
        else:
            # If no, then scrape the data using scraper, then add to voting poll.
            pass
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
            filter.append({
                "Topic.value": t
            })
        print(filter)
        vids = list(db['video_dataset'].find({
            "$or": filter
        }, {'_id': 0}))

        return json.dumps(vids)

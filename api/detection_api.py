from flask_restful import Api, Resource, reqparse
from api.detection_code.detect import detect
import pymongo


class DetectionAPIHandler(Resource):
    def get(self):
        return {
            'resultStatus': 'SUCCESS',
            'message': "Hello Api Handler : GET Request"
        }

    def post(self):
        print(self)
        parser = reqparse.RequestParser()
        # parser.add_argument('type', type=str)
        parser.add_argument('url', type=str)
        parser.add_argument('topic', type=str)

        args = parser.parse_args()

        print(args)
        # note, the post req from frontend needs to match the strings here (e.g. 'type and 'message')
        videoID = args['url'].split('?v=')[1].split('&')[0]
        try:
            print(args['url'], videoID, args['topic'])
            detection = detect(videoID, args['topic'])
        except:
            detection = "No Captions present for the video"
        db = pymongo.MongoClient('localhost:27017')['YT_Misinfo_Dataset']
        existing_vid = db['Video_Dataset'].find_one({
            "Video_ID": videoID
        }, {'_id': 0})

        final_ret = {
            "status": "Error" if isinstance(detection, str) else "Success",
            "detection": detection,
            "voting": existing_vid['voting'] if existing_vid and 'voting' in existing_vid.keys() else {},
            "Title": existing_vid['Title'] if existing_vid and 'Title' in existing_vid.keys() else "Do you think the video is wrongly classified?",
        }
        print(final_ret)
        return final_ret

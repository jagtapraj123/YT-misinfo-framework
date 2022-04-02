from flask_restful import Api, Resource, reqparse
from api.detection_code.detect import detect
import pymongo
import requests
from urllib.parse import urlparse
import os


class DetectionAPIHandler(Resource):
    def post(self):
        print(self)
        parser = reqparse.RequestParser()
        parser.add_argument('url', type=str)
        parser.add_argument('topic', type=str)

        args = parser.parse_args()

        print(args)
        url = args['url']
        pattern = '"playabilityStatus":{"status":"ERROR","reason":"Video unavailable"'
        try:
            request = requests.get(url)
            url = request.url
            if request.status_code != 200 or pattern in request.text:
                return {
                    "status": "Error",
                    "url": url,
                    "reason": "URL is not a valid YouTube video."
                }
        except:
            return {
                "status": "Error",
                "url": url,
                "reason": "Error parsing URL. Check if valid URL is entered."
            }

        try:
            website = urlparse(url).netloc
            website = website.lower().split('.')
            print(website)
            if "youtube" not in website:
                return {
                    "status": "Error",
                    "url": url,
                    "reason": "URL is not a YouTube URL."
                }
        except:
            return {
                "status": "Error",
                "url": url,
                "reason": "Error parsing URL. Check if valid YouTube video URL is entered."
            }

        videoID = url.split('?v=')[1].split('&')[0]
        
        mongo_uri = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
        db = pymongo.MongoClient(mongo_uri)['YT_Misinfo_Dataset']
        existing_vid = db['Video_Dataset'].find_one({
            "Video_ID": videoID
        }, {'_id': 0})

        try:
            print(url, videoID, args['topic'])
            detection = detect(videoID, args['topic'])
            if isinstance(detection, str):
                return {
                    "status": "Error",
                    "url": url,
                    "reason": detection
                }
            return {
                "status": "Success",
                "url": url,
                "detection": detection,
                "voting": existing_vid['voting'] if existing_vid and 'voting' in existing_vid.keys() else {},
                "Title": existing_vid['Title'] if existing_vid and 'Title' in existing_vid.keys() else "Do you think the video is wrongly classified?",
            }
        except:
            return {
                "status": "Error",
                "url": url,
                "reason": "Error while classifying video. Check if video is in English."
            }

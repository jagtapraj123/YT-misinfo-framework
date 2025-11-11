# https://towardsdatascience.com/build-deploy-a-react-flask-app-47a89a5d17d9
# https://cloud.google.com/community/tutorials/building-flask-api-with-cloud-firestore-and-deploying-to-cloud-run
from flask import Flask, send_from_directory, jsonify
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS  # comment this on deployment
from api.detection_api import DetectionAPIHandler
from api.dataset_api import DatasetGetterAPIHandler, DatasetUpdaterAPIHandler, DatasetExtractAPIHandler, DatasetTopicsAPIHandler, BasicVideoCheckingAPIHandler
import os
import redis

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app)  # comment this on deployment
api = Api(app)

redis_host = os.environ.get("REDIS_HOST", "redis")
redis_client = redis.Redis(host=redis_host, port=6379, db=0)


@app.route("/", defaults={'path': ''})
def serve(path):
    redis_client.incr("num_webpage_visits")
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/stats')
def stats():
    webpage_visits = redis_client.get("num_webpage_visits")
    videos_classified = redis_client.get("num_videos_classified")
    dataset_retrieved = redis_client.get("num_dataset_retrieved")
    dataset_updated = redis_client.get("num_dataset_updated")
    return jsonify({
        "webpage_visits": int(webpage_visits) if webpage_visits else 0,
        "videos_classified": int(videos_classified) if videos_classified else 0,
        "dataset_retrieved": int(dataset_retrieved) if dataset_retrieved else 0,
        "dataset_updated": int(dataset_updated) if dataset_updated else 0,
    })


api.add_resource(DetectionAPIHandler, '/detect')
api.add_resource(DatasetGetterAPIHandler, '/getDataset')
api.add_resource(DatasetTopicsAPIHandler, '/getTopics')
api.add_resource(DatasetUpdaterAPIHandler, '/updateDataset')
api.add_resource(BasicVideoCheckingAPIHandler, '/checkVideo')
api.add_resource(DatasetExtractAPIHandler, '/extractDataset')

if __name__ == '__main__':
    # app.run(debug=True)
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)

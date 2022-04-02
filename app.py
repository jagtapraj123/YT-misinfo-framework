# https://towardsdatascience.com/build-deploy-a-react-flask-app-47a89a5d17d9
# https://cloud.google.com/community/tutorials/building-flask-api-with-cloud-firestore-and-deploying-to-cloud-run
from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS  # comment this on deployment
from api.detection_api import DetectionAPIHandler
from api.dataset_api import DatasetGetterAPIHandler, DatasetUpdaterAPIHandler, DatasetExtractAPIHandler, DatasetTopicsAPIHandler, BasicVideoCheckingAPIHandler
import os

app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app)  # comment this on deployment
api = Api(app)


@app.route("/", defaults={'path': ''})
def serve(path):
    return send_from_directory(app.static_folder, 'index.html')


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

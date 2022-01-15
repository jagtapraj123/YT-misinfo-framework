from flask_restful import Api, Resource, reqparse
from api.detection_code.detect import detect

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

        try:
            print(args['url'], args['topic'])
            detection = detect(args['url'], args['topic'])
        except:
            detection = False

        final_ret = {"status": "Success", "detection": detection}
        print(final_ret)
        return final_ret

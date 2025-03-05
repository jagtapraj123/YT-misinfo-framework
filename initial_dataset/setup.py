import json
import pymongo
import os

MONGODB_URI = f"mongodb://{os.environ['MONGODB_USERNAME']}:{os.environ['MONGODB_PASSWORD']}@{os.environ['MONGODB_HOSTNAME']}:27017/{os.environ['MONGODB_DATABASE']}?authSource=admin"

def setupDataset(db, col, file):
    data = []
    with open(file, 'r') as f:
        data = json.loads(f.read())

    # mongo_uri = f"mongodb://{os.environ['MONGODB_USERNAME']}:{os.environ['MONGODB_PASSWORD']}@{os.environ['MONGODB_HOSTNAME']}:27017/{os.environ['MONGODB_DATABASE']}?authSource=admin"
    # mongo_uri = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
    print(MONGODB_URI)
    db = pymongo.MongoClient(MONGODB_URI)[db]
    collection = db[col]

    present, added = 0, 0
    for vid in data:
        existing_vid = collection.find_one(
            {
                "vid_url": vid['vid_url'],
            }
        )
        if not existing_vid:
            added += 1
            print(vid['vid_url'])
            collection.find_one_and_update(
                {
                    "vid_url": vid['vid_url'],
                },
                {
                    "$set": vid,
                },
                upsert = True
            )
        else:
            present += 1

    print("Added {} videos, {} videos were already present.".format(added, present))

def setupTagMapping(db, col, file):
    data = []
    with open(file, 'r') as f:
        data = json.loads(f.read())

    # mongo_uri = f"mongodb://{os.environ['MONGODB_USERNAME']}:{os.environ['MONGODB_PASSWORD']}@{os.environ['MONGODB_HOSTNAME']}:27017/{os.environ['MONGODB_DATABASE']}?authSource=admin"
    # mongo_uri = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
    print(MONGODB_URI)
    db = pymongo.MongoClient(MONGODB_URI)[db]
    collection = db[col]

    topics = set()
    tags = set()
    for vid in data:
        print(vid["vid_url"])
        if 'Topic' in vid.keys():
            topics.add(vid['Topic']['name'])
            tags.add(vid['Topic']['value'])
            collection.find_one_and_update(
                {
                    "tag": vid['Topic']['value'],
                },
                {
                    "$addToSet": { "topics": vid['Topic']['name'] },
                },
                upsert = True
            )
        # else:
        #     tags.add(vid['Topic']['value'])
        #     collection.find_one_and_update(
        #         {
        #             "tag": vid['Topic']['value'],
        #         },
        #         {
        #             "$set": { "topics": [] },
        #         },
        #         upsert = True
        #     )

        if 'tags' in vid:
            for tag in vid['tags']:
                tags.add(tag)
                collection.find_one_and_update(
                    {
                        "tag": tag,
                    },
                    {
                        "$setOnInsert": {"topics": []},
                    },  # Only sets an empty list if the document is new
                    upsert=True
                )

    print("Added {} tags and {} topics.".format(len(tags), len(topics)))

if __name__ == '__main__':
    setupDataset(os.environ['MONGODB_DATABASE'], "Video_Dataset", "Video_Dataset.json")
    setupTagMapping(os.environ['MONGODB_DATABASE'], "Topics_Mapping", "Video_Dataset.json")
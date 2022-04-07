import json
import pymongo

def setupDataset(db, col, file):
    data = []
    with open(file, 'r') as f:
        data = json.loads(f.read())

    db = pymongo.MongoClient('localhost:27017')[db]
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

    db = pymongo.MongoClient('localhost:27017')[db]
    collection = db[col]

    topics = set()
    tags = set()
    for vid in data:
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
        else:
            tags.add(vid['Topic']['value'])
            collection.find_one_and_update(
                {
                    "tag": vid['Topic']['value'],
                },
                {
                    "$set": { "topics": [] },
                },
                upsert = True
            )

    print("Added {} tags and {} topics.".format(len(tags), len(topics)))

if __name__ == '__main__':
    setupDataset("YT_Misinfo_Dataset", "Video_Dataset", "Video_Dataset.json")
    setupTagMapping("YT_Misinfo_Dataset", "Topics_Mapping", "Video_Dataset.json")
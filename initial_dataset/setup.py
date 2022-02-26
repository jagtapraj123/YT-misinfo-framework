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

if __name__ == '__main__':
    setupDataset("YT_Misinfo_Dataset", "Video_Dataset", "Video_Dataset.json")
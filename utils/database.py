import os
import pymongo as mg

if os.environ.get('IN_DOCKER') is not None:
    MONGO_HOST = 'mongodb'
else:
    MONGO_HOST = '0.0.0.0'
    # print('For development purposes you need to have a mongo docker running')
    # print('e.g.')
    # print('sudo docker run -d -p 27017:27017 -v ~/data:/data/db mongo')
    # print('good luck')

def get_db():
    client = mg.MongoClient(MONGO_HOST, 27017)

    # Access or create
    db = client['yolo_db']
    collection = db['seen_images']

    return collection

def insert_objects(image_hash, scores):
    collection = get_db()
    mongopost = {
                'image_hash' : image_hash,
                'scores' : scores
                }
    collection.insert_one(mongopost)

def load_scores(image_hash):
    collection = get_db()
    scores = collection.find_one({'image_hash' : image_hash})

    return scores


import cv2
import urllib
import numpy as np
from flask import Flask
from flask import request
from flask import jsonify
from utils import image as ui
from utils import database as ud
from pydarknet import Detector, Image

def get_detector():
    net = Detector(bytes("yolo/yolov3.cfg", encoding="utf-8"),
                   bytes("yolo/yolov3.weights", encoding="utf-8"),
                   0,
                   bytes("yolo/coco.data", encoding="utf-8"))

    return net

app = Flask(__name__)
YOLO = get_detector()

@app.route('/objects', methods=['POST'])
def detect_objects():
    # Download the image or a random cat picture
    data = request.json
    default_url = 'http://thecatapi.com/api/images/get?format=src&type=jpg'
    url = data.get('url', default_url)
    resp = urllib.request.urlopen(url)

    # TODO No budget for error handling
    assert resp.code == 200

    # Make it digestible by the YOLO  
    img = np.asarray(bytearray(resp.read()), dtype="uint8")

    # TODO Assert that this is RGB ...
    img = cv2.imdecode(img, -1)

    # ... and change to BGR anyway
    img = img[:,:,::-1] 

    # There are better ways to do this: e.g. xxhash
    # May not be worth the struggle for image-sized arrays
    image_hash = ui.make_hash(img)

    # Only Look Once at an image
    loaded = ud.load_scores(image_hash)

    if loaded is not None:
        scores = loaded['scores']
    else:
        # Nothing is stored
        yolo_image = Image(img)
        results = YOLO.detect(yolo_image)

        # Prepare the response
        objects = []
        for it, result in enumerate(results):
            an_object = yolo2filestack(result)
            objects.append(an_object)

        # JSONified list of detected records
        scores = {'objects' : objects}
        ud.insert_objects(image_hash, scores)

    return jsonify(scores)

def yolo2filestack(result):
    # Decode the results
    category = result[0].decode("utf-8")
    confidence = int(100 * result[1])
    x, y, w, h = result[2]

    # x, y are centered in the yolo output
    # filestack uses x1 and y1 ...
    x = x - w/2
    y = y - h/2
    # ... and integers
    x, y = int(x), int(y)
    w, h = int(w), int(h)

    bounding_box = {
                    'x' : x,
                    'y' : y,
                    'w' : w,
                    'h' : h
                   }

    # This is the structure of a single record
    out = {
            'object' : category,
            'confidence' : confidence,
            'bounding_box' : bounding_box
          }

    return out

if __name__ == '__main__':
    app.run(host='0.0.0.0')

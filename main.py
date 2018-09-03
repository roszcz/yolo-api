import cv2
import urllib
import requests
import numpy as np
from io import BytesIO
from flask import Flask
from flask import request
from flask import jsonify
from pydarknet import Detector, Image

def get_detector():
    net = Detector(bytes("yolo/yolov3.cfg", encoding="utf-8"),
                   bytes("yolo/yolov3.weights", encoding="utf-8"),
                   0,
                   bytes("yolo/coco.data", encoding="utf-8"))

    return net

app = Flask(__name__)
net = get_detector()

@app.route('/objects', methods=['POST'])
def detect_objects():
    data = request.json
    default_url = "https://raw.githubusercontent.com/madhawav/darknet/master/data/dog.jpg"
    url = data.get('url', default_url)
    resp = urllib.request.urlopen(url)
    assert resp.code == 200

    img = np.asarray(bytearray(resp.read()), dtype="uint8")

    # TODO Assert that this is RGB ...
    img = cv2.imdecode(img, -1)

    # ... and change to BGR
    img = img[:,:,::-1] 

    # There are better ways to do this: e.g. xxhash
    img_hash = hash(img.tostring())

    yolo_image = Image(img)
    results = net.detect(yolo_image)

    objects = []
    for it, result in enumerate(results):
        # key = 'object_{}'.format(it)
        an_object = yolo2filestack(result)
        objects.append(an_object)

    out = {'objects' : objects}
    return jsonify(out)

def yolo2filestack(result):
    # Decode the results
    category = result[0].decode("utf-8")
    confidence = int(100 * result[1])
    x, y, w, h = result[2]

    # x, y are centered in the yolo output
    # filestack uses x1 and y1
    x = x - w/2
    x = int(x)

    y = y - h/2
    y = int(y)

    w, h = int(w), int(h)

    bounding_box = {'x' : x, 'y' : y, 'w' : w, 'h' : h}

    out = {
            'object' : category,
            'confidence' : confidence,
            'bounding_box' : bounding_box
          }

    return out

if __name__ == '__main__':
    app.run(host='0.0.0.0')

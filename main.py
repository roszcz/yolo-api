import urllib
from flask import Flask
from flask import request
from flask import jsonify
from utils import yolo as uy
from utils import image as ui
from utils import database as ud


app = Flask(__name__)
YOLO = uy.YOLO()


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
    img = ui.response2image(resp)

    # There are better ways to do this: e.g. xxhash
    # May not be worth the struggle for image-sized arrays
    image_hash = ui.make_hash(img)

    # Only Look Once at an image
    loaded = ud.load_scores(image_hash)

    if loaded is not None:
        scores = loaded['scores']
    else:
        # Nothing is stored
        scores = YOLO.detect_objects(img)

        # JSONified list of detected records
        ud.insert_objects(image_hash, scores)

    return jsonify(scores)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

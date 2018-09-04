from pydarknet import Detector, Image


class YOLO(object):
    def __init__(self):
        # https://pjreddie.com/darknet/yolo/
        self.net = Detector(bytes("yolo/yolov3.cfg", encoding="utf-8"),
                            bytes("yolo/yolov3.weights", encoding="utf-8"),
                            0,
                            bytes("yolo/coco.data", encoding="utf-8"))

    def detect_objects(self, img):
        # Digestable by the darknet
        yolo_image = Image(img)
        results = self.net.detect(yolo_image)

        # Prepare the response
        objects = []
        for it, result in enumerate(results):
            an_object = yolo2filestack(result)
            objects.append(an_object)

        scores = {'objects' : objects}

        return scores


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


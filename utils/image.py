import imagehash
from PIL import Image

def make_hash(img_array):
    image_pil = Image.fromarray(img_array)
    image_hash = imagehash.dhash(image_pil)
    image_hash = str(image_hash)

    return image_hash

def response2image(resp):
    # Assert that this is RGB ...
    img = np.asarray(bytearray(resp.read()), dtype="uint8")
    img = cv2.imdecode(img, -1)

    # ... and change to BGR anyway
    img = img[:,:,::-1] 

    return img

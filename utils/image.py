import imagehash
from PIL import Image

def make_hash(img_array):
    image_pil = Image.fromarray(img_array)
    image_hash = imagehash.dhash(image_pil)
    image_hash = str(image_hash)

    return image_hash

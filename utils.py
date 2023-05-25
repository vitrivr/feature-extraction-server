
import base64
import io
from PIL import Image

def prepare_images(images):
    return_list = True
    image_strs = images
    if type(images) is str:
        image_strs = [image_strs]
        return_list = False
    images = []
    for img_string in image_strs:
        if img_string.startswith('data:image'):
            img_string = img_string.split(',', 1)[1]
        img_data = base64.b64decode(img_string)
        image = Image.open(io.BytesIO(img_data))
        if image.mode != "RGB":
            image = image.convert(mode="RGB")
        images.append(image)
    return images, return_list

def prepare_text(text):
    return_list = True
    text = text
    if type(text) is str:
        text = [text]
        return_list = False
    return text, return_list
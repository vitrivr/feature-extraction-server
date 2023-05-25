from utils import prepare_images, prepare_text


def caption(func):
    def inner(image, inference_args={}):
        image, return_list = prepare_images(image)
        result = func(image, inference_args)
        if not return_list:
            result = result[0]
        return result
    return inner

def conditional_caption(func):
    def inner(image, text, inference_args={}):
        image, return_list = prepare_images(image)
        result = func(image, text, inference_args)
        if not return_list:
            result = result[0]
        return result
    return inner

tasks = {
    "caption": caption,
    "conditional_caption": conditional_caption
}

default_models = {"caption": "blip", "conditional_caption": "blip"}
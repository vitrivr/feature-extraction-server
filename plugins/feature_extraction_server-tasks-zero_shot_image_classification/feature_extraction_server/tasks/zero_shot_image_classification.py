from feature_extraction_server.core.utils import prepare_images

def wrap(func):
    def inner(image, classes, config ={}):
        image, return_list = prepare_images(image)
        result = func(image, classes, config)
        if not return_list:
            result = result[0]
        return result
    return inner
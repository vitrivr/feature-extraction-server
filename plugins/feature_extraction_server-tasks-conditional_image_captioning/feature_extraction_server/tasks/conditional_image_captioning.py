from feature_extraction_server.core.utils import prepare_multiple

def wrap(func):
    def inner(image, text, config={}):
        data, return_list = prepare_multiple(image=image, text=text)
        image = data['image']
        text = data['text']
        result = func(image, text, config)
        if not return_list:
            result = result[0]
        return result
    return inner
from feature_extraction_server.core.utils import prepare_text

def wrap(func):
    def inner(text, config={}):
        text, return_list = prepare_text(text)
        result = func(text, config)
        if not return_list:
            result = result[0]
        return result
    return inner
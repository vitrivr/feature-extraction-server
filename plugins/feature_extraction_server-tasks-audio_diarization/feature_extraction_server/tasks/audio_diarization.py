from feature_extraction_server.core.utils import prepare_audio

def wrap(func):
    def inner(audio, config={}):
        audio, return_list = prepare_audio(audio)
        result = func(audio, config)
        if not return_list:
            result = result[0]
        return result
    return inner
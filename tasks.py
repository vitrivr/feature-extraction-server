from utils import prepare_images, prepare_text, prepare_audio


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

def automated_speech_recognition(func):
    def inner(audio, inference_args={}):
        audio, return_list = prepare_audio(audio)
        result = func(audio, inference_args)
        if not return_list:
            result = result[0]
        return result
    return inner

tasks = {
    "caption": caption,
    "conditional_caption": conditional_caption,
    "automated_speech_recognition": automated_speech_recognition
}

default_models = {"caption": "blip2", "conditional_caption": "blip2", "automated_speech_recognition": "whisper"}
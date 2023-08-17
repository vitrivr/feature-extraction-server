from feature_extraction_server.utils import prepare_images, prepare_multiple, prepare_text, prepare_audio


def image_embedding(func):
    def inner(image, config={}):
        image, return_list = prepare_images(image)
        result = func(image, config)
        if not return_list:
            result = result[0]
        return result
    return inner

def text_embedding(func):
    def inner(text, config={}):
        text, return_list = prepare_text(text)
        result = func(text, config)
        if not return_list:
            result = result[0]
        return result
    return inner
    

def image_captioning(func):
    def inner(image, config={}):
        image, return_list = prepare_images(image)
        result = func(image, config)
        if not return_list:
            result = result[0]
        return result
    return inner

def zero_shot_image_classification(func):
    def inner(image, classes, config ={}):
        image, return_list = prepare_images(image)
        result = func(image, classes, config)
        if not return_list:
            result = result[0]
        return result
    return inner

def conditional_image_captioning(func):
    def inner(image, text, config={}):
        data, return_list = prepare_multiple(image=image, text=text)
        image = data['image']
        text = data['text']
        result = func(image, text, config)
        if not return_list:
            result = result[0]
        return result
    return inner

def automated_speech_recognition(func):
    def inner(audio, config={}):
        audio, return_list = prepare_audio(audio)
        result = func(audio, config)
        if not return_list:
            result = result[0]
        return result
    return inner

def object_detection(func):
    def inner(image, config={}):
        image, return_list = prepare_images(image)
        result = func(image, config)
        if not return_list:
            result = result[0]
        return result
    return inner

def optical_character_recognition(func):
    def inner(image, config=None):
        image, return_list = prepare_images(image)
        result = func(image, config)
        if not return_list:
            result = result[0]
        return result
    return inner

def face_embedding(func):
    def inner(image, config={}):
        image, return_list = prepare_images(image)
        result = func(image, config)
        if not return_list:
            result = result[0]
        return result
    return inner

def zero_shot_object_detection(func):
    def inner(image, classes, config={}):
        image, return_list = prepare_images(image)
        result = func(image, classes, config)
        if not return_list:
            result = result[0]
        return result
    return inner

def audio_diarization(func):
    def inner(audio, config={}):
        audio, return_list = prepare_audio(audio)
        result = func(audio, config)
        if not return_list:
            result = result[0]
        return result
    return inner

tasks = {
    "image_captioning": image_captioning,
    "conditional_image_captioning": conditional_image_captioning,
    "automated_speech_recognition": automated_speech_recognition,
    "object_detection": object_detection,
    "image_embedding": image_embedding,
    "text_embedding": text_embedding,
    "optical_character_recognition": optical_character_recognition,
    "zero_shot_image_classification": zero_shot_image_classification,
    "zero_shot_object_detection": zero_shot_object_detection,
    "face_embedding": face_embedding, 
    "audio_diarization": audio_diarization,
}

default_models = {
    "image_captioning": "blip2", 
    "conditional_image_captioning": "blip2", 
    "automated_speech_recognition": "whisper", 
    "object_detection": "detr-resnet101",
    "image_embedding": "clip-vit-large-patch14",
    "text_embedding": "clip-vit-large-patch14",
    "optical_character_recognition": "easyocr",
    "zero_shot_image_classification": "clip-vit-large-patch14",
    "zero_shot_object_detection": "owlvit-base-patch32",
    "audio_diarization": "pyannote"
    }
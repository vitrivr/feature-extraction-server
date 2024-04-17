from feature_extraction_server.core.dataformat import *

import psutil
import os


def get_memory_usage():
    # Get the process id of the current process
    pid = os.getpid()

    # Create a Process object
    current_process = psutil.Process(pid)

    # Get the memory info of the current process
    memory_info = current_process.memory_info()
    
    ret = ""
     
    ret += f"RSS (Resident Set Size): {memory_info.rss / (1024 ** 2):.2f} MB"
    ret += '\t'
    ret += f"VMS (Virtual Memory Size): {memory_info.vms / (1024 ** 2):.2f} MB"

    return ret

import traceback

def log_exception(logger, exception):
    debug_msg = ''
    for line in traceback.format_exception(type(exception), exception, exception.__traceback__):
        debug_msg += line + '\n'
    logger.debug(debug_msg)

def prepare_images(images):
    image_strs, return_list = prepare_text(images)
    images = []
    for img_string in image_strs:
        images.append(IImageFormat.from_data_url(img_string))
    return images, return_list

def prepare_audio(audio_data_url):
    audio_data, return_list = prepare_text(audio_data_url)
    audio = []
    for audio_string in audio_data:
        audio.append(IAudioFormat.from_data_url(audio_string))
    return audio, return_list

def prepare_text(text):
    return_list = True
    text = text
    if type(text) is str:
        text = [text]
        return_list = False
    return text, return_list

def prepare_multiple(**dict):
    text = dict.get('text', None)
    images = dict.get('image', None)
    audio = dict.get('audio', None)
    
    output = {}
    return_list = False
    
    if text:
        text, return_list_text = prepare_text(text)
        output['text'] = text
        return_list = return_list or return_list_text
    if images:
        images, return_list_images = prepare_images(images)
        output['image'] = images
        return_list = return_list or return_list_images
    if audio:
        audio, return_list_audio = prepare_audio(audio)
        output['audio'] = audio
        return_list = return_list or return_list_audio
    
    max_len = max([len(output[key]) for key in output])
    
    for key in output:
        factor = max_len // len(output[key])
        output[key] = output[key] * factor
    
    return output, return_list

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]
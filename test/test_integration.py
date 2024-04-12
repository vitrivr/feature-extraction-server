import sys
sys.path.append('./feature_extraction_server-core/') 
import os

for dir in os.listdir('./plugins/'):
    sys.path.append(f'./plugins/{dir}/')

import pytest
import base64
import soundfile as sf
import io
import requests
import json
import time
# from feature_extraction_server.core.utils import prepare_multiple

def test_tasks_list(base_url):
    response = requests.get(f'{base_url}/tasks')

    assert response.status_code == 200

    # Check response body
    tasks = response.json()

    # Check if response is a list
    assert isinstance(tasks, list)

    # Check if list contains at least one string
    assert len(tasks) > 0
    assert isinstance(tasks[0], str)

@pytest.fixture
def base_url():
    return 'http://localhost:8888/api'

loaded = {}

def data_base64_fixture(loader_func):
    @pytest.fixture
    def data_base64(request):
        param = request.param

        if not isinstance(param, list):
            if param in loaded:
                return loaded[param]
            data = loader_func(param)
            loaded[param] = data
            return data

        ret = []
        for path in param:
            if path in loaded:
                ret.append(loaded[path])
                continue
            data = loader_func(path)
            loaded[path] = data
            ret.append(data)
        return ret
    return data_base64

def load_image_file(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def load_audio_file(audio_file):
    samples, samplerate = sf.read(audio_file)
    output = io.BytesIO()
    sf.write(output, samples, samplerate, format='WAV')
    b_64 = base64.b64encode(output.getvalue()).decode('ascii')
    return f"data:audio/wav;base64,{b_64}"

image_data_base64 = data_base64_fixture(load_image_file)
audio_data_base64 = data_base64_fixture(load_audio_file)


# def check_output_shape(response_data, inner, **kwargs):
#     data, is_list = prepare_multiple(**kwargs)
#     n = len(data[list(kwargs)[0]])
    
    
#     if is_list:
#         # Check if response is a list
#         assert isinstance(response_data, list)
#         assert(len(response_data) == n)
    
#         for elem in response_data:
#             inner(elem)
#     else:
#         inner(response_data)
        


@pytest.mark.parametrize("model,config", [("blip", {"top_k": 50}), ("vit-gpt2", {}), ("blip2", {})])
@pytest.mark.parametrize("image_data_base64", ["test/data/1.png"], indirect=True)
def test_image_captioning(image_data_base64, model, config, base_url):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "image": image_data_base64,
        "config": config
    }
    
    new_job_response = requests.post(f'{base_url}/tasks/image-captioning/{model}/jobs', headers=headers, data=json.dumps(payload))
    
    # Check status code
    assert new_job_response.status_code == 200
    
    new_job_id = new_job_response.json()["id"]
    
    while True:
        response = requests.get(f'{base_url}/tasks/image-captioning/jobs/{new_job_id}')
        
        assert response.status_code == 200
        
        response_data = response.json()
        
        if response_data["status"] == "complete":
            break
        
        time.sleep(1)
    
    def check_response(element):
        assert isinstance(element, str)
    
    check_response(response_data["result"]["caption"])

image_caption_prompt1 = "Question: What is depicted in this image? Answer:"
image_caption_prompt2 = "Question: What is the significance of this image? Answer:"
conditional_image_captioning_test_cases = [
    ("test/data/1.png", image_caption_prompt1)
]

@pytest.mark.parametrize("model,config", [("blip", {}), ("blip2", {})])
@pytest.mark.parametrize("image_data_base64,text", conditional_image_captioning_test_cases, indirect=["image_data_base64"])
def test_conditional_image_captioning(image_data_base64, text, model, config, base_url):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "image": image_data_base64,
        "text": text,
        "config": config
    }
    
    new_job_response = requests.post(f'{base_url}/tasks/conditional-image-captioning/{model}/jobs', headers=headers, data=json.dumps(payload))
    
    # Check status code
    assert new_job_response.status_code == 200
    
    new_job_id = new_job_response.json()["id"]
    
    while True:
        response = requests.get(f'{base_url}/tasks/conditional-image-captioning/jobs/{new_job_id}')
        
        assert response.status_code == 200
        
        response_data = response.json()
        
        if response_data["status"] == "complete":
            break
        
        time.sleep(1)
    
    response_data = response.json()
    
    def check_response(element):
        assert isinstance(element, str)
    
    check_response(response_data["result"]["caption"])

classes = ["photo", "document"]
zero_shot_image_classification_test_cases = [
    ("test/data/1.png", classes),
    (["test/data/1.png"], classes), 
    (["test/data/1.png", "test/data/1.png"], classes),
]
    
@pytest.mark.parametrize("model,config", [("clip_vit_large_patch14", {})])
@pytest.mark.parametrize("image_data_base64,classes", zero_shot_image_classification_test_cases, indirect=["image_data_base64"])
def test_zero_shot_image_classification(image_data_base64, classes, model, config, base_url):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "image": image_data_base64,
        "classes": classes,
        "config": config
    }
    
    new_job_response = requests.post(f'{base_url}/tasks/zero-shot-image-classification/{model}/jobs', headers=headers, data=json.dumps(payload))
    
    # Check status code
    assert new_job_response.status_code == 200
    
    new_job_id = new_job_response.json()["id"]
    
    while True:
        response = requests.get(f'{base_url}/tasks/zero-shot-image-classification/jobs/{new_job_id}')
        
        assert response.status_code == 200
        
        response_data = response.json()
        
        if response_data["status"] == "complete":
            break
        
        time.sleep(1)
        
    
    def check_response(element):
        assert isinstance(element, list)
        assert len(element) == len(classes)
        assert isinstance(element[0], float)
    
    check_response(response_data["result"]["probabilities"])

@pytest.mark.parametrize("model,config", [("clip_vit_large_patch14", {})])
@pytest.mark.parametrize("image_data_base64", ["test/data/1.png", ["test/data/1.png"], ["test/data/1.png", "test/data/1.png"]], indirect=True)
def test_image_embedding(image_data_base64, model, config, base_url):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "image": image_data_base64,
        "config": config
    }
    
    new_job_response = requests.post(f'{base_url}/tasks/image-embedding/{model}/jobs', headers=headers, data=json.dumps(payload))
    
    # Check status code
    assert new_job_response.status_code == 200
    
    new_job_id = new_job_response.json()["id"]
    
    while True:
        response = requests.get(f'{base_url}/tasks/image-embedding/jobs/{new_job_id}')
        
        assert response.status_code == 200
        
        response_data = response.json()
        
        if response_data["status"] == "complete":
            break
        
        time.sleep(1)
        
    def check_response(element):
        assert isinstance(element, list)
        assert isinstance(element[0], float)
    
    check_response(response_data["result"]["embedding"])


@pytest.mark.parametrize("model,config", [("whisper", {})])
@pytest.mark.parametrize("audio_data_base64", ["test/data/beach-german.mp3"], indirect=True)
def test_automated_speech_recognition(base_url, audio_data_base64, model, config):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "audio": audio_data_base64,
        "config": config
    }
    
    new_job_response = requests.post(f'{base_url}/tasks/automated-speech-recognition/{model}/jobs', headers=headers, data=json.dumps(payload))
    
    # Check status code
    assert new_job_response.status_code == 200
    
    new_job_id = new_job_response.json()["id"]
    
    while True:
        response = requests.get(f'{base_url}/tasks/automated-speech-recognition/jobs/{new_job_id}')
        
        assert response.status_code == 200
        
        response_data = response.json()
        
        if response_data["status"] == "complete":
            break
        
        time.sleep(1)
    
    def check_response(element):
        assert isinstance(element, str)
    
    check_response(response_data["result"]["transcript"])
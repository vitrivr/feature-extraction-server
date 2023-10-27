import pytest
import base64
import soundfile as sf
import io
import requests
import json
from feature_extraction_server.core.utils import prepare_multiple

def test_get_tasks(base_url):
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
    return 'http://localhost:5000'

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
    return base64.b64encode(output.getvalue()).decode('ascii')

image_data_base64 = data_base64_fixture(load_image_file)
audio_data_base64 = data_base64_fixture(load_audio_file)


def check_output_shape(response_data, inner, **kwargs):
    data, is_list = prepare_multiple(**kwargs)
    n = len(data[list(kwargs)[0]])
    
    
    if is_list:
        # Check if response is a list
        assert isinstance(response_data, list)
        assert(len(response_data) == n)
    
        for elem in response_data:
            inner(elem)
    else:
        inner(response_data)
        


@pytest.mark.parametrize("model,config", [("blip", {"top_k": 50}), ("vit-gpt2", {}), ("blip2", {})])
@pytest.mark.parametrize("image_data_base64", ["test/data/1.png", ["test/data/1.png"], ["test/data/1.png", "test/data/1.png"]], indirect=True)
def test_image_captioning(image_data_base64, model, config, base_url):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "task": "image_captioning",
        "image": image_data_base64,
        "model": model,
        "config": config
    }
    
    response = requests.post(f'{base_url}/extract', headers=headers, data=json.dumps(payload))
    
    # Check status code
    assert response.status_code == 200
    
    response_data = response.json()
    
    def check_response(element):
        assert isinstance(element, list)
        assert len(element) == 1
        assert isinstance(element[0], str)
    
    check_output_shape(response_data, check_response, image=image_data_base64)

image_caption_prompt1 = "Question: What is depicted in this image? Answer:"
image_caption_prompt2 = "Question: What is the significance of this image? Answer:"
conditional_image_captioning_test_cases = [
    ("test/data/1.png", image_caption_prompt1),
    (["test/data/1.png"], image_caption_prompt1), 
    (["test/data/1.png", "test/data/1.png"], image_caption_prompt1),
    ("test/data/1.png", [image_caption_prompt1, image_caption_prompt2])
]

@pytest.mark.parametrize("model,config", [("blip", {}), ("blip2", {})])
@pytest.mark.parametrize("image_data_base64,text", conditional_image_captioning_test_cases, indirect=["image_data_base64"])
def test_conditional_image_captioning(image_data_base64, text, model, config, base_url):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "task": "conditional_image_captioning",
        "image": image_data_base64,
        "model": model,
        "text": text,
        "config": config
    }
    
    response = requests.post(f'{base_url}/extract', headers=headers, data=json.dumps(payload))
    
    # Check status code
    assert response.status_code == 200
    
    response_data = response.json()
    
    def check_response(element):
        assert isinstance(element, list)
        assert len(element) == 1
        assert isinstance(element[0], str)
    
    check_output_shape(response_data, check_response, image=image_data_base64, text=text)

classes = ["photo", "document"]
zero_shot_image_classification_test_cases = [
    ("test/data/1.png", classes),
    (["test/data/1.png"], classes), 
    (["test/data/1.png", "test/data/1.png"], classes),
]
    
@pytest.mark.parametrize("model,config", [("clip-vit-large-patch14", {})])
@pytest.mark.parametrize("image_data_base64,classes", zero_shot_image_classification_test_cases, indirect=["image_data_base64"])
def test_zero_shot_image_classification(image_data_base64, classes, model, config, base_url):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "task": "zero_shot_image_classification",
        "image": image_data_base64,
        "model": model,
        "classes": classes,
        "config": config
    }
    
    response = requests.post(f'{base_url}/extract', headers=headers, data=json.dumps(payload))
    
    # Check status code
    assert response.status_code == 200
    
    response_data = response.json()
    
    def check_response(element):
        assert isinstance(element, list)
        assert len(element) == len(classes)
        assert isinstance(element[0], float)
    
    check_output_shape(response_data, check_response, image=image_data_base64)

@pytest.mark.parametrize("model,config", [("clip-vit-large-patch14", {})])
@pytest.mark.parametrize("image_data_base64", ["test/data/1.png", ["test/data/1.png"], ["test/data/1.png", "test/data/1.png"]], indirect=True)
def test_image_embedding(image_data_base64, model, config, base_url):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "task": "image_embedding",
        "image": image_data_base64,
        "model": model,
        "config": config
    }
    
    response = requests.post(f'{base_url}/extract', headers=headers, data=json.dumps(payload))
    
    assert response.status_code == 200
    
    response_data = response.json()
    
    def check_response(element):
        assert isinstance(element, list)
        assert isinstance(element[0], float)
    
    check_output_shape(response_data, check_response, image=image_data_base64)
import base64
import os
import requests
import json

paths = ['1.png', '2.jpg', '3.png', '4.jpg']
images = []

for path in paths:
    with open(os.path.join("test_images",path), 'rb') as file:
        img = base64.b64encode(file.read()).decode('utf-8')
        images.append(img)



# Create a dictionary to send as JSON in the request
#data = {'task': 'caption','image': images, 'model':'blip', 'inference_args': {'max_length': 32, 'do_sample':True, "top_k":50, "top_p":0.95, "temperature":0.5}}


response = requests.get('http://localhost:5000/tasks')

for task in response.json()['tasks']:
    mresponse = requests.get(f'http://localhost:5000/models/{task}')
    for model in mresponse.json()['models']:
        print(f'Task: {task} - Model: {model}')

# Send the POST request
# response = requests.post('http://localhost:5000/extract', json={'task': 'caption','image': images, 'model':'vit-gpt2'})
# # Print the response
# print(response.json())

# Send the POST request
response = requests.post('http://localhost:5000/extract', json={'task': 'conditional_caption', 'model': 'mplug-owl-llama-7b','image': images, "text": "What is depicted in this photograph?"})
# Print the response
print(response.json())
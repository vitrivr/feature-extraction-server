import base64
import requests
import json

paths = ['test-image.jpg', 'test-image2.jpg']
images = []

for path in paths:
    with open(path, 'rb') as file:
        img = base64.b64encode(file.read()).decode('utf-8')
        images.append(img)



# Create a dictionary to send as JSON in the request
data = {'task': 'caption','image': images}

# Send the POST request
response = requests.post('http://localhost:5000/extract', json=data)

# Print the response
print(response.json())
import requests
import unittest
import json
import base64
import soundfile as sf
import io

class TestImageCaptioningAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:5000'
        self.endpoint = '/extract'

        with open("test_data/1.png", "rb") as img_file:
            self.base64_string_1 = base64.b64encode(img_file.read()).decode('utf-8')
        
        with open("test_data/2.jpg", "rb") as img_file:
            self.base64_string_2 = base64.b64encode(img_file.read()).decode('utf-8')
        
        with open("test_data/gettysburg.wav", "rb") as audio_file:
            samples, samplerate = sf.read(audio_file)
            output = io.BytesIO()
            sf.write(output, samples, samplerate, format='WAV')
            self.base64_string_3 = base64.b64encode(output.getvalue()).decode('ascii')
        
        with open("test_data/beach-german.mp3", "rb") as audio_file:
            samples, samplerate = sf.read(audio_file)
            output = io.BytesIO()
            sf.write(output, samples, samplerate, format='WAV')
            self.base64_string_4 = base64.b64encode(output.getvalue()).decode('ascii')        


    def test_get_tasks(self):
        response = requests.get(f'{self.base_url}/tasks')

        # Check status code
        self.assertEqual(response.status_code, 200)

        # Check response body
        tasks = response.json()

        # Check if response is a list
        self.assertIsInstance(tasks, list)

        # Check if list contains at least one string
        self.assertIsInstance(tasks[0], str)
    
    # def test_get_models(self):
    #     # Assuming that 'image_captioning' task exists.
    #     task = 'image_captioning'
    #     response = requests.get(f'{self.base_url}/models/{task}')

    #     # Check status code
    #     self.assertEqual(response.status_code, 200)

    #     # Check response body
    #     models = response.json()

    #     # Check if response is a list
    #     self.assertIsInstance(models, list)

    #     # Check if list contains at least one string
    #     self.assertIsInstance(models[0], str)
    
    def test_image_captioning(self):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "task": "image_captioning",
            "image": self.base64_string_1,
            "model": "blip",
            "config": {"top_k": 50}
        }
        
        response = requests.post(f'{self.base_url}{self.endpoint}', headers=headers, data=json.dumps(payload))
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Check response body
        response_data = response.json()

        # Check if response is a list
        self.assertIsInstance(response_data, list)

        # Check if list contains at least one string
        self.assertIsInstance(response_data[0], str)
    
    def test_image_captioning_batched(self):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "task": "image_captioning",
            "image": [self.base64_string_1, self.base64_string_2],
            "model": "blip",
            "config": {"top_k": 50}
        }
        
        response = requests.post(f'{self.base_url}{self.endpoint}', headers=headers, data=json.dumps(payload))
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Check response body
        response_data = response.json()

        # Check if response is a list
        self.assertIsInstance(response_data, list)

        # Check if list contains two lists
        self.assertIsInstance(response_data[0], list)
        self.assertIsInstance(response_data[1], list)
        
        # Check if each list contains at least one string
        self.assertIsInstance(response_data[0][0], str)
        self.assertIsInstance(response_data[1][0], str)

    def test_conditional_image_captioning(self):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "task": "conditional_image_captioning",
            "image": self.base64_string_1,
            "text": "What is depicted in this photograph?"
        }
        
        response = requests.post(f'{self.base_url}{self.endpoint}', headers=headers, data=json.dumps(payload))
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Check response body
        response_data = response.json()

        # Check if response is a list
        self.assertIsInstance(response_data, list)

        # Check if list contains at least one string
        self.assertIsInstance(response_data[0], str)
    
    def test_batched_conditional_image_captioning(self):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "task": "conditional_image_captioning",
            "image": [self.base64_string_1, self.base64_string_2],
            "text": ["What is depicted in this photograph?", "What is depicted in this photograph?"]
        }
        
        response = requests.post(f'{self.base_url}{self.endpoint}', headers=headers, data=json.dumps(payload))
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Check response body
        response_data = response.json()

        # Check if response is a list
        self.assertIsInstance(response_data, list)

        # Check if list contains two lists
        self.assertIsInstance(response_data[0], list)
        self.assertIsInstance(response_data[1], list)
        
        # Check if each list contains at least one string
        self.assertIsInstance(response_data[0][0], str)
        self.assertIsInstance(response_data[1][0], str)
    
    def test_semi_batched_conditional_image_captioning(self):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "task": "conditional_image_captioning",
            "image": [self.base64_string_1, self.base64_string_2],
            "text": "What is depicted in this photograph?"
        }
        response = requests.post(f'{self.base_url}{self.endpoint}', headers=headers, data=json.dumps(payload))
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Check response body
        response_data = response.json()

        # Check if response is a list
        self.assertIsInstance(response_data, list)

        # Check if list contains two lists
        self.assertIsInstance(response_data[0], list)
        self.assertIsInstance(response_data[1], list)
        
        # Check if each list contains at least one string
        self.assertIsInstance(response_data[0][0], str)
        self.assertIsInstance(response_data[1][0], str)
    
    def test_automated_speech_recognition(self):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "task": "automated_speech_recognition",
            "audio": self.base64_string_3
        }
        
        response = requests.post(f'{self.base_url}{self.endpoint}', headers=headers, data=json.dumps(payload))
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Check response body
        response_data = response.json()

        # Check if response is a string
        self.assertIsInstance(response_data, str)
    
    def test_batched_automated_speech_recognition(self):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "task": "automated_speech_recognition",
            "audio": [self.base64_string_3, self.base64_string_4]
        }
        response = requests.post(f'{self.base_url}{self.endpoint}', headers=headers, data=json.dumps(payload))
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Check response body
        response_data = response.json()

        # Check if response is a list
        self.assertIsInstance(response_data, list)
        
        # Check if list contains two strings
        self.assertIsInstance(response_data[0], str)
        self.assertIsInstance(response_data[1], str)
    
    def test_zero_shot_image_classification(self):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "task": "zero_shot_image_classification",
            "image": self.base64_string_1,
            "classes": ["animal", "human", "plant"]
        }
        
        response = requests.post(f'{self.base_url}{self.endpoint}', headers=headers, data=json.dumps(payload))
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Check response body
        response_data = response.json()
        
        # Check if response is a list
        self.assertIsInstance(response_data, list)
        
        # Check if list contains at least one float
        self.assertIsInstance(response_data[0], float)
        
        # Check if length is equal to number of classes
        self.assertEqual(len(response_data), 3)
    
    def test_batched_zero_shot_image_classification(self):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "task": "zero_shot_image_classification",
            "image": [self.base64_string_1, self.base64_string_2],
            "classes" : ["animal", "human", "plant"]
        }
        response = requests.post(f'{self.base_url}{self.endpoint}', headers=headers, data=json.dumps(payload))
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Check response body
        response_data = response.json()
        
        # Check if response is a list
        self.assertIsInstance(response_data, list)
        
        # Check if list contains two lists
        self.assertIsInstance(response_data[0], list)
        self.assertIsInstance(response_data[1], list)
        
        # Check if each list contains at least one float
        self.assertIsInstance(response_data[0][0], float)
        self.assertIsInstance(response_data[1][0], float)
        
        # Check if length is equal to number of classes
        self.assertIsInstance(response_data[0], list)
        self.assertIsInstance(response_data[1], list)
        
    def test_object_detection(self):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "task": "object_detection",
            "image": self.base64_string_1
        }
        
        response = requests.post(f'{self.base_url}{self.endpoint}', headers=headers, data=json.dumps(payload))
        
        # Check status code
        self.assertEqual(response.status_code, 200)
        
        # Check response body
        response_data = response.json()
        
        # Check if response is a dictionary
        self.assertIsInstance(response_data, dict)
        
        # Check if dictionary contains boxes, labels and scores
        self.assertIn("boxes", response_data)
        self.assertIn("labels", response_data)
        self.assertIn("scores", response_data)
        
        # Check if boxes, labels and scores are lists
        self.assertIsInstance(response_data["boxes"], list)
        self.assertIsInstance(response_data["labels"], list)
        self.assertIsInstance(response_data["scores"], list)
        
        # Check if boxes, labels and scores are of equal length
        l = len(response_data["boxes"])
        self.assertEqual(l, len(response_data["labels"]))
        self.assertEqual(l, len(response_data["scores"]))
        
        # Check if all boxes have four float coordinates
        for box in response_data["boxes"]:
            self.assertEqual(len(box), 4)
            self.assertIsInstance(box[0], float)
        
        # Check if all labels are strings
        for label in response_data["labels"]:
            self.assertIsInstance(label, str)
        
        
        
        
if __name__ == '__main__':
    unittest.main()

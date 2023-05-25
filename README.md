# Feature Extraction Server

This server accepts both images and text as input and performs various AI tasks, such as image captioning. It uses a modular design that allows new tasks and models to be easily added.

## Usage


### Server Side

In order to perform captioning or other tasks, the server must first be started. As a prerequisite, install the required packages:
```bash
pip install -r environment.yml
```

To run the server, simply run app.py:

```bash
python app.py
```

The server will start running on localhost on port 5000.

### Captioning
To caption an image, send a POST request to the `/extract` endpoint with a JSON body. The JSON should have the key 'task' set to 'caption' and a key of 'image' set to a base64 encoded image string or a list of such strings. The encoded strings can optionally have a data URL prefix (for example: `data:image/png;base64,iVBORw0KGgoA...`) It can optionally contain 'model' to specify the model, and 'inference_args' to specify any additional arguments. If the input corresponds to a single image the server will return a list of captions for the image. If the input was a list of images the server will return a list of lists (one list for each image in the input). Depending on the model, the inference arguments can be used to specify the number of captions per image.

Example of captioning an image with curl:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"image": "<base64-encoded-image>", "task": "caption", "model": "blip", "inference_args": {"top_k":50}}' http://localhost:5000/extract
```

this returns 

```json
['a black and white photo of a house']
```

### Conditional Captioning
Conditional captioning is also supported. Just include a 'text' key in the request json with a single string.


## Extending the Server

The server is designed to be easily extensible with new tasks and models. To add a new task or model, follow these steps:

1. **Add a new task**: To add a new task, edit the tasks module so that it implements a wrapper function. Make sure you also update the `tasks` dictionary and the `default_models` dictionary (also in the tasks module).

2. **Add a new model**: To add a new model, simply add a new Python file in the models directory. For each task that this model is able to do you can implement a function that is named after the task.

For example, if you want to add a new image classification model, you might create a new file called 'cool_model.py'. In 'cool_model.py', you would define your classification function like this:

```python
def classify_image(image, other_arg, more_args):
    # Your model's image classification code here
    pass
```
Of course, make sure to edit the tasks module if the task 'classify_image' does not exist yet. 
Once you set everything up, you can specify 'classify_image' as the task and 'cool_model' as the model in your POST request to the /extract endpoint.

## API Endpoints

- **POST /extract**: Perform extraction with the specified task (or default task) and model (or default model). All other arguments will be passed to the task wrapper which wraps the models functions.

- **GET /tasks**: Get a list of all available tasks.

- **GET /models/\<task>**: Get a list of all models available for the specified task.
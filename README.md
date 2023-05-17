# Feature Extraction Server

This server accepts both images and text as input and performs various AI tasks, such as image captioning. It uses a modular design that allows new tasks and models to be easily added.

## Usage

### Client Side

To use the server, send a POST request to the `/extract` endpoint with a JSON body. The JSON should have a key of 'image' or 'text' containing base64 encoded image strings or text strings respectively. The image can be encoded directly or have a data URL prefix (for example: `data:image/png;base64,iVBORw0KGgoA...`) These can be single strings or lists of strings. The server will return a single response or a list of responses that correspond to the input data. Note that depending on the task or on additional arguments (see below) each element could itself be a list.

It can optionally contain 'task' (default: 'caption') to specify the task, 'model' to specify the model, and 'extraction_args' to specify any additional arguments.

Example of using the server with curl:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"image": "<base64-encoded-image>", "task": "caption", "model": "model_name", "extraction_args": {"arg1": value1}}' http://localhost:5000/extract
```

### Server Side

Install the required packages:
```bash
pip install -r environment.yml
```

To run the server, simply run app.py:

```bash
python app.py
```

The server will start running on localhost on port 5000.

## Extending the Server

The server is designed to be easily extensible with new tasks and models. To add a new task or model, follow these steps:

1. **Add a new task**: To add a new task, create a new directory with the task name in the same directory as app.py. In this new directory, add a Python file for each model you want to add to the task. Make sure to include an `__init__.py` file that has a global variable called `default_model` of type string. 

2. **Add a new model to an existing task**: To add a new model to an existing task, simply add a new Python file in the corresponding task directory. The Python file should define an extract function that takes in data and extraction arguments and returns the extraction result.

For example, if you want to add a new image classification model, you might create a new directory called 'classify' and add a file my_model.py in it. In my_model.py, you would define your extract function like this:

```python
def extract(data, extraction_args):
    # Your model's inference code here
    pass
```
Then, you can specify 'classify' as the task and 'my_model' as the model in your POST request to the /extract endpoint.

## API Endpoints

- **POST /extract**: Perform extraction with the specified or default task and model. Accepts 'image' or 'text' for data, and optionally 'task', 'model', and 'inference_args' in the JSON body. The 'image' or 'text' can be a single string or a list of strings. The response will be a single string or a list of strings that correspond to the input data.

- **GET /tasks**: Get a list of all available tasks.

- **GET /models/\<task>**: Get a list of all models available for the specified task.
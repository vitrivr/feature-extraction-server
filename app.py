import io, os
from flask import Flask, request, jsonify
import base64
from PIL import Image
from importlib import import_module

app = Flask(__name__)


# Define a list of available tasks
tasks = ['caption']
default_task = 'caption'

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/models/<task>', methods=['GET'])
def get_models(task):
    if task not in tasks:
        return jsonify({'error': 'Invalid task'}), 400

    try:
        task_dir = os.path.join(os.getcwd(), task)
        models = [name[:-3] for name in os.listdir(task_dir) if os.path.isfile(os.path.join(task_dir, name)) and name.endswith('.py') and name != '__init__.py']
    except FileNotFoundError:
        return jsonify({'error': 'Task directory not found'}), 400

    return jsonify({'models': models})


@app.route('/extract', methods=['POST'])
def extract():
    data = None
    try:
        if len([key for key in request.json.keys() if key in ['image', 'text']]) != 1:
            raise Exception('Either image or text must be provided')
        if 'image' in request.json:
            return_list = True
            image_strs = request.json['image']
            if type(request.json['image']) is str:
                image_strs = [image_strs]
                return_list = False
            images = []
            for img_string in image_strs:
                img_data = base64.b64decode(img_string)
                image = Image.open(io.BytesIO(img_data))
                if image.mode != "RGB":
                    image = image.convert(mode="RGB")
                images.append(image)
            data = images
        
        if 'text' in request.json:
            return_list = True
            text = request.json['text']
            if type(request.json['text']) is str:
                text = [text]
                return_list = False
            data = text

        # Get the task
        task = request.json.get('task', default_task)
        task_module = import_module(task)
        
        if not task in tasks:
            raise Exception(f'Task {task} not found')
        
        # Check if extraction_args is in the request
        extraction_args = request.json.get('extraction_args', {})
        model_name = request.json.get('model', task_module.default_model)
        
        # Load the module and import the extract function
        try:
            model_module = import_module(f'{task}.{model_name}')
            extract = model_module.extract
        except ImportError:
            return jsonify({'error': 'Model not found'}), 400
        except AttributeError:
            return jsonify({'error': 'extract function not found in the model module'}), 400
        
        extraction = extract(data, extraction_args)
        if not return_list:
            extraction = extraction[0]
        return jsonify({'message': extraction})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, app)

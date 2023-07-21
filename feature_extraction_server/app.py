import io, os
from flask import Flask, request, jsonify
import base64
from PIL import Image
from importlib import import_module
from tasks import tasks, default_models

application = Flask(__name__)

default_task = 'caption'

@application.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(list(tasks))

# @application.route('/models/<task>', methods=['GET'])
# def get_models(task):
#     if task not in tasks:
#         return jsonify({'error': 'Invalid task'}), 400

#     models_dir = os.path.join(os.getcwd(), "feature_extraction_server/models")
#     models = []
#     for name in os.listdir(models_dir):
#         if os.path.isfile(os.path.join(models_dir, name)) and name.endswith('.py') and name != '__init__.py':
#             try:
#                 module = import_module(f'models.{name[:-3]}')
#                 if task in module.__dict__:
#                     models.append(name[:-3])
#             except Exception as e:
#                 pass

#     return jsonify(models)


@application.route('/extract', methods=['POST'])
def extract():
    try:
        # Get the task
        task = request.json.get('task', default_task)
        if not task in tasks:
            raise Exception(f'Task {task} not found')
        # Check if model is in the request
        model_name = request.json.get('model', default_models[task])
        
        kwargs = {**request.json}
        kwargs.pop('task', None)
        kwargs.pop('model', None)
        
        # Load the module and import the extract function
        try:
            model_module = import_module(f'models.{model_name}')
            extract = tasks[task](getattr(model_module, task))
        except ImportError as e:
            return jsonify({'error': 'Model not found'}), 400
        except AttributeError:
            return jsonify({'error': f'extract function not found in the {model_name} module'}), 400
        
        response = jsonify(extract(**kwargs))
        print(response.get_data())
        return response

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, application)
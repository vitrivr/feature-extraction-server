from functools import wraps
from flask import Flask, request, jsonify
import logging
from feature_extraction_server.tasks import tasks, default_models
import feature_extraction_server.settings as settings
from werkzeug.exceptions import BadRequest, NotFound
from feature_extraction_server.ipc import ModelProcessManager

application = Flask(__name__)

mpm = None

@application.route('/tasks', methods=['GET'])
def get_tasks():
    logging.info('Endpoint /tasks called')
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


def get_model_name_and_task():
    task = request.json.get('task', settings.DEFAULT_TASK)
    _validate_task(task)
    model_name = request.json.get('model', default_models.get(task))
    return model_name, task
def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logging.info(f'Endpoint {request.path} called')
            return func(*args, **kwargs)
        except BadRequest as e:
            msg = f"Bad request: {str(e)}"
            logging.error(msg)
            return jsonify({'error': msg}), 400
        except NotFound as e:
            msg = f"Resource not found: {str(e)}"
            logging.error(f"msg")
            return jsonify({'error': msg}), 404
        except Exception as e:
            msg = f"Unexpected error: {str(e)}"
            logging.error(msg)
            return jsonify({'error': msg}), 500
    return wrapper

@application.route('/extract', methods=['POST'])
@handle_exceptions
def extract():
    model_name, task = get_model_name_and_task()
    
    kwargs = {**request.json}
    kwargs.pop('task', None)
    kwargs.pop('model', None)
    
    job_id = mpm.add_job(model_name, task, kwargs)
    response = jsonify(mpm.get_result(model_name, job_id))
    logging.info('Response sent')
    logging.debug(f'Response: {response}')

    return response

@application.route('/load', methods=['POST'])
@handle_exceptions
def load():
    model_name, _ = get_model_name_and_task()
    mpm.start_process(model_name)
    mpm.await_running(model_name)
    return jsonify({'status': 'ok'})

@application.route('/free', methods=['POST'])
@handle_exceptions
def free():
    model_name, _ = get_model_name_and_task()
    mpm.remove_process(model_name)
    mpm.await_stopped(model_name)
    return jsonify({'status': 'ok'})


def _validate_task(task):
    if task not in tasks:
        logging.error(f"Task {task} not found")
        raise NotFound(f"Task {task} not found")


def entrypoint():
    global mpm
    logging.basicConfig(level= settings.LOG_LEVEL)
    logger = logging.getLogger(__name__)
    
    file_handler = logging.FileHandler(settings.LOG_PATH)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    
    logging.debug('Starting application')
    mpm = ModelProcessManager()
    
    
    
    return application



    

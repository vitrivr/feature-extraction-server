import logging
from flask import request, jsonify
from functools import wraps

from feature_extraction_server.core.utils import log_exception

from feature_extraction_server.core.exceptions import NoDefaultTaskException, NoDefaultModelException, ModelNotFoundException, TaskNotFoundException, ModelAlreadyStartedException

logger = logging.getLogger(__name__)


def add_settings(settings_manager):
    pass

def add_routes(application_interface, flask_app):
    flask_app.route('/legacy/tasks', methods=['GET'], endpoint ="tasks")(handle_exceptions(list_all_tasks, application_interface))
    flask_app.route('/legacy/extract', methods=['POST'], endpoint="extract")(handle_exceptions(extract, application_interface))
    
    

def handle_exceptions(func, application_interface):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f'Endpoint {request.path} called')
            result = func(application_interface, *args, **kwargs)
            logger.debug(f'Endpoint {request.path} returned successfully')
            
            return result
        except (NoDefaultTaskException, NoDefaultModelException) as e:
            msg = f"Bad request: {str(e)}"
            log_exception(logger, e)
            return jsonify({'error': msg}), 400
        except (ModelNotFoundException, TaskNotFoundException) as e:
            msg = f"Resource not found: {str(e)}"
            log_exception(logger, e)
            return jsonify({'error': msg}), 404
        except Exception as e:
            msg = f"Unexpected error: {str(e)}"
            logger.error(msg)
            log_exception(logger, e)
            return jsonify({'error': msg}), 500
    
    return wrapper

def list_all_tasks(application_interface):
    return jsonify(list(application_interface.list_all_task_names()))

def extract(application_interface):
    json = request.json
    model_name = json.pop('model', None)
    task_name = json.pop('task', None)
    model_interface = application_interface.get_model(model_name = model_name, task_name = task_name)
    try:
        model_interface.start()
    except ModelAlreadyStartedException:
        pass
    
    job = application_interface.create_job(model_name = model_name, task_name = task_name, kwargs = json)
    job.start()
    return jsonify(job.get_result())


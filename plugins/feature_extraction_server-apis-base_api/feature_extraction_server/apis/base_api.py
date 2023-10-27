import logging
from flask import request, jsonify
from functools import wraps

from feature_extraction_server.core.utils import log_exception

from feature_extraction_server.core.exceptions import NoDefaultTaskException, NoDefaultModelException, ModelNotFoundException, TaskNotFoundException, ModelAlreadyStartedException

logger = logging.getLogger(__name__)


def add_settings(settings_manager):
    pass

def add_routes(application_interface, flask_app):
    flask_app.route('/api/tasks/list', methods=['GET'])(handle_exceptions(list_all_tasks, application_interface))
    flask_app.route('/api/models/list', methods=['GET'])(handle_exceptions(list_all_models, application_interface))
    flask_app.route('/api/models/<model>/tasks/list', methods=['GET'])(handle_exceptions(list_all_tasks_for_model, application_interface))
    flask_app.route('/api/tasks/<task>/models/list', methods=['GET'])(handle_exceptions(list_all_models_for_task, application_interface))
    flask_app.route('/api/models/<model>/tasks/<task>/features', methods=['POST'])(handle_exceptions(model_task_features, application_interface))
    flask_app.route('/api/tasks/<task>/models/<model>/features', methods=['POST'])(handle_exceptions(task_model_features, application_interface))
    flask_app.route('/api/tasks/<task>/features', methods=['POST'])(handle_exceptions(task_features, application_interface))
    flask_app.route('/api/models/<model>/start', methods=['POST'])(handle_exceptions(start_model, application_interface))
    flask_app.route('/api/models/<model>/stop', methods=['POST'])(handle_exceptions(stop_model, application_interface))
    
    

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

def model_task_features(application_interface, model, task):
    return features(application_interface, task, model)

def task_model_features(application_interface, task, model):
    return features(application_interface, task, model)

def task_features(application_interface, task):
    return features(application_interface, task)

def features(application_interface, task, model = None):
    model_interface = application_interface.get_model(model_name = model, task_name = task)
    try:
        model_interface.start()
    except ModelAlreadyStartedException:
        pass
    
    job = application_interface.create_job(model, task, request.json)
    job.start()
    return jsonify(job.get_result())

def list_all_tasks(application_interface):
    return jsonify(list(application_interface.list_all_task_names()))

def list_all_models(application_interface):
    return jsonify(list(application_interface.list_all_model_names()))

def list_all_tasks_for_model(application_interface, model):
    return jsonify(list(application_interface.list_tasks_for_model(model)))

def list_all_models_for_task(application_interface, task):
    return jsonify(list(application_interface.list_models_for_task(task)))

def start_model(application_interface, model):
    application_interface.get_model(model).start()
    return jsonify({'status': 'ok'})

def stop_model(application_interface, model):
    application_interface.get_model(model).stop()
    return jsonify({'status': 'ok'})

from feature_extraction_server.services.extraction_backend import ExtractionBackend
from feature_extraction_server.services.fast_api_app import FastApiApp
from feature_extraction_server.core.exceptions import ModelAlreadyStartedException
import logging
from fastapi import Body
from simple_plugin_manager.service import Service

logger = logging.getLogger(__name__)


def wrap_function(func, args, input_model, output_model):
    if not input_model is None:
        async def wrapped_function(*, data : input_model = Body(...)) -> output_model:
            return func(*args, dict(data))
    else:
        async def wrapped_function() -> output_model:
            return func(*args)
    return wrapped_function
    

class BaseApi(Service):
    
    @staticmethod
    def initialize_service(extraction_backend: ExtractionBackend, fast_api_app: FastApiApp):
        baseapi = BaseApi(extraction_backend=extraction_backend)
        baseapi.add_routes(fast_api_app.app)
        return baseapi
    
    def __init__(self, extraction_backend):
        self._extraction_backend = extraction_backend
    
    def add_routes(self, app):
        
        app.get('/api/tasks/list', name="list_all_tasks")(wrap_function(self._list_all_tasks, [], None, list))
        
        app.get('/api/models/list', name="list_all_models")(wrap_function(self._list_all_models, [], None, list))
        
        for model in self._extraction_backend.iterate_models():
            app.get(f'/api/models/{model.name}/tasks/list', name=f"list_all_tasks_for_{model.name}")(wrap_function(self._list_all_tasks_for_model, [model.name], None, list))
            app.post(f'/api/models/{model.name}/start', name=f"start_{model.name}")(wrap_function(self._start_model, [model.name], None, None))
            app.post(f'/api/models/{model.name}/stop', name=f"stop_{model.name}")(wrap_function(self._stop_model, [model.name], None, None))
        
        for task in self._extraction_backend.iterate_tasks():
            app.get(f'/api/tasks/{task.name}/models/list', name=f"list_all_models_for_{task.name}")(wrap_function(self._list_all_models_for_task, [task.name], None, list))
            app.post(f'/api/tasks/{task.name}/features', name=f"features_{task.name}")(wrap_function(self._features, [task.name], task.get_input_schema(), task.get_output_schema()))
            
        for model in self._extraction_backend.iterate_models():
            for task in model.iterate_tasks():
                app.post(f'/api/models/{model.name}/tasks/{task.name}/features', name=f"features_{model.name}_{task.name}")(wrap_function(self._features, [task.name, model.name], task.get_input_schema(), task.get_output_schema()))
                app.post(f'/api/tasks/{task.name}/models/{model.name}/features', name=f"features_{task.name}_{model.name}")(wrap_function(self._features, [task.name, model.name], task.get_input_schema(), task.get_output_schema()))

    def _features(self, task, model=None, json_data={}):
        model_interface = self._extraction_backend.get_model(model_name=model, task_name=task)
        try:
            model_interface.start()
        except ModelAlreadyStartedException:
            pass
        
        job = self._extraction_backend.create_job(model, task, json_data)
        job.start()
        return job.get_result()

    def _list_all_tasks(self):
        task_names = []
        for task in self._extraction_backend.iterate_tasks():
            task_names.append(task.name)
        return task_names

    def _list_all_models(self):
        model_names = []
        for model in self._extraction_backend.iterate_models():
            model_names.append(model.name)
        return model_names

    def _list_all_tasks_for_model(self, model):
        task_names = []
        app_model = self._extraction_backend.get_model(task_name=None, model_name = model)
        for task in app_model.iterate_tasks():
            task_names.append(task.name)
        return task_names

    def _list_all_models_for_task(self, task):
        model_names = []
        app_task = self._extraction_backend.get_task(task)
        for model in app_task.iterate_models():
            model_names.append(model.name)
        return model_names

    def _start_model(self, model):
        self._extraction_backend.get_model(task_name=None, model_name=model).start()
        return

    def _stop_model(self, model):
        self._extraction_backend.get_model(task_name=None , model_name = model).stop()
        return 

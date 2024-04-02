
from feature_extraction_server.services.extraction_backend import ExtractionBackend
from feature_extraction_server.services.fast_api_app import FastApiApp
from feature_extraction_server.core.exceptions import ModelAlreadyStartedException
import logging
from fastapi import Body
from simple_plugin_manager.service import Service

from simple_plugin_manager.settings import EnumSetting, NoValue, MissingConfigurationException
from feature_extraction_server.services.extraction_backend import ExtractionBackend
from feature_extraction_server.services.default_models_service import DefaultModelsService
from simple_plugin_manager.services.settings_manager import SettingsManager
from feature_extraction_server.services.model_namespace import ModelNamespace
from feature_extraction_server.services.task_namespace import TaskNamespace

logger = logging.getLogger(__name__)


def wrap_function(func, args, input_model, output_model):
    if not input_model is None:
        async def wrapped_function(*, data : input_model = Body(...)) -> output_model:
            return func(*args, dict(data))
    else:
        async def wrapped_function() -> output_model:
            return func(*args)
    return wrapped_function
    

class DefaultModelsApi(Service):
    
    @staticmethod
    def initialize_service(default_models_service:DefaultModelsService, extraction_backend: ExtractionBackend, fast_api_app: FastApiApp):
        
        
        baseapi = DefaultModelsApi(extraction_backend=extraction_backend, default_models_service=default_models_service)
        baseapi.add_routes(fast_api_app.app)
        return baseapi
    
    def __init__(self, extraction_backend, default_models_service):
        self._extraction_backend = extraction_backend
        self.default_models_service = default_models_service
    
    def add_routes(self, app):
        
        for task in self._extraction_backend.iterate_tasks():
            app.add_api_route(f'/api/tasks/{task.name}/features', wrap_function(self._features, [task.name], task.get_input_schema(), task.get_output_schema()), methods=['POST'], name=f"features", tags=[task.name])
            
    
    def _features(self, task, json_data={}):
        model, task = self.default_models_service.apply_defaults(None, task)
        model_interface = self._extraction_backend.get_model(model_name=model)
        try:
            model_interface.start()
        except ModelAlreadyStartedException:
            pass
        
        job = self._extraction_backend.create_job(model, task, json_data)
        job.start()
        return job.get_result()
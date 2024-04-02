import logging
logger = logging.getLogger(__name__)

from feature_extraction_server.core.exceptions import NoDefaultTaskException, NoDefaultModelException
from simple_plugin_manager.settings import EnumSetting, NoValue, MissingConfigurationException
from simple_plugin_manager.services.settings_manager import SettingsManager
from feature_extraction_server.services.model_namespace import ModelNamespace
from feature_extraction_server.services.task_namespace import TaskNamespace
from simple_plugin_manager.service import Service


class DefaultModelsService(Service):
    
    @staticmethod
    def initialize_service(task_namespace: TaskNamespace, model_namespace:ModelNamespace, settings_manager:SettingsManager):
        
        default_models = {}
        for task_name in task_namespace.iter_module_names():
            default_model_setting = EnumSetting(f"DEFAULT_MODEL_{task_name.upper()}", NoValue , list(model_namespace.iter_module_names()) , f"The default model for the task {task_name}.")
            settings_manager.add_setting(default_model_setting)
            try:
                default_models[task_name] = default_model_setting.get()
            except MissingConfigurationException:
                pass
        
        default_task_setting = EnumSetting("DEFAULT_TASK", NoValue, list(task_namespace.iter_module_names()) , "The default task to run.")
        try:
            default_task = default_task_setting.get()
        except MissingConfigurationException:
            default_task = None
        settings_manager.add_setting(default_task_setting)
        
        return DefaultModelsService(default_task, default_models)
    
    def __init__(self, default_models, default_task):
        self.default_models = default_models
        self.default_task = default_task
    
    def apply_defaults(self, model_name, task_name):
        if task_name is None:
            task_name = self.default_task
        if model_name is None:
            if task_name is None:
                error_msg = "task_name must be set if no default task is set."
                logger.warn(error_msg)
                raise NoDefaultTaskException(error_msg)
            try:
                model_name = self.default_models[task_name]
            except KeyError:
                error_msg = f"model_name must be set if no default model is set for task {task_name}."
                logger.warn(error_msg)
                raise NoDefaultModelException(error_msg)
        return model_name, task_name
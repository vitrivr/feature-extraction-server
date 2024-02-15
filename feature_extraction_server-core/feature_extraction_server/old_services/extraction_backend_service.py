from feature_extraction_server.services.namespace_service import ModelNamespace, TaskNamespace
from feature_extraction_server.core.settings import SettingsManager, EnumSetting, NoValue, MissingConfigurationException, FloatSetting
from feature_extraction_server.core.builders import JobBuilder, ModelBuilder, TaskBuilder
from feature_extraction_server.core.extraction_backend import ExtractionBackend
from injector import provider, Module, singleton



import logging
logger = logging.getLogger(__name__)

class ExtractionBackendService(Module):
    
    @singleton
    @provider
    def provide_extraction_backend(self, settings_manager : SettingsManager, model_namespace : ModelNamespace, task_namespace : TaskNamespace, job_builder : JobBuilder) -> ExtractionBackend:
        logger.debug("Initializing ExtractionBackend")
        result_check_interval_setting = FloatSetting("RESULT_CHECK_INTERVAL", 0.1, "The interval in seconds between checks for the result of a job.")
        settings_manager.add_setting(result_check_interval_setting)
        
        
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
        
        return ExtractionBackend(
            job_builder=job_builder,
            task_namespace= task_namespace,
            model_namespace=model_namespace,
            result_check_interval=result_check_interval_setting.get(),
            default_task=default_task,
            default_models=default_models
        )

from feature_extraction_server.core.application_interface import ApplicationInterface
from feature_extraction_server.core.components.component import Component
from feature_extraction_server.core.settings import FloatSetting, EnumSetting, NoValue, MissingConfigurationException
from feature_extraction_server.core.components.job_builder_component import JobBuilderComponent
from feature_extraction_server.core.components.startable_model_builder_component import StartableModelBuilderComponent
from feature_extraction_server.core.components.namespace_components import TaskNamespaceComponent, ModelNamespaceComponent
from feature_extraction_server.core.components.settings_manager_component import SettingsManagerComponent


import logging
logger = logging.getLogger(__name__)



class ApplicationInterfaceComponent(Component):
    
    @staticmethod
    def _init():
        logger.debug("Initializing ApplicationInterface")
        settings_manager = SettingsManagerComponent.get()
        result_check_interval_setting = FloatSetting("RESULT_CHECK_INTERVAL", 0.1, "The interval in seconds between checks for the result of a job.")
        settings_manager.add_setting(result_check_interval_setting)
        
        
        model_namespace = ModelNamespaceComponent.get()
        default_models = {}
        for task_name in TaskNamespaceComponent.get().iter_plugin_names():
            default_model_setting = EnumSetting(f"DEFAULT_MODEL_{task_name.upper()}", NoValue , list(model_namespace.iter_plugin_names()) , f"The default model for the task {task_name}.")
            settings_manager.add_setting(default_model_setting)
            try:
                default_models[task_name] = default_model_setting.get()
            except MissingConfigurationException:
                pass
        
        task_namespace = TaskNamespaceComponent.get()
        default_task_setting = EnumSetting("DEFAULT_TASK", NoValue, list(task_namespace.iter_plugin_names()) , "The default task to run.")
        try:
            default_task = default_task_setting.get()
        except MissingConfigurationException:
            default_task = None
        settings_manager.add_setting(default_task_setting)
        
        return ApplicationInterface(
            job_builder=JobBuilderComponent.get(),
            startable_model_builder=StartableModelBuilderComponent.get(),
            task_namespace=TaskNamespaceComponent.get(),
            model_namespace=ModelNamespaceComponent.get(),
            result_check_interval=result_check_interval_setting.get(),
            default_task=default_task,
            default_models=default_models
        )

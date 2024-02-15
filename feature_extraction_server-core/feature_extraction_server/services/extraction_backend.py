import logging
logger = logging.getLogger(__name__)

from feature_extraction_server.core.exceptions import MissingTaskImplementationException, NoDefaultTaskException, NoDefaultModelException
from simple_plugin_manager.settings import FloatSetting, EnumSetting, NoValue, MissingConfigurationException
from simple_plugin_manager.service import Service
from simple_plugin_manager.services.settings_manager import SettingsManager
from simple_plugin_manager.service_manager import ServiceManager
from feature_extraction_server.services.job_builder import JobBuilder
from feature_extraction_server.services.model_namespace import ModelNamespace
from feature_extraction_server.services.task_namespace import TaskNamespace



class ExtractionBackend(Service):
    
    @staticmethod
    def initialize_service(settings_manager : SettingsManager, model_namespace : ModelNamespace, task_namespace : TaskNamespace, job_builder : JobBuilder, service_manager: ServiceManager):
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
            default_models=default_models,
            service_manager=service_manager
        )
        
    class JobInterface:
        def __init__(self, job, result_check_interval):
            self._job = job
            self._result_check_interval = result_check_interval
        
        def start(self):
            self._job.start()
        
        def get_result(self):
            return self._job.get_result(self._result_check_interval)
    
    class ModelInterface:
        def __init__(self, model, extraction_backend):
            self._model = model
            self.name = model.name
            self._extraction_backend = extraction_backend
        
        def iterate_tasks(self):
            for task_name in self._extraction_backend._task_namespace.iter_module_names():
                try:
                    self._model.get_task_implementation(task_name)
                except MissingTaskImplementationException:
                    continue
                yield ExtractionBackend.TaskInterface(task = self._extraction_backend._task_namespace.instantiate_plugin(task_name), extraction_backend = self._extraction_backend)
        
        def start(self):
            self._model.start()
        
        def stop(self):
            self._model.stop()
    
    class TaskInterface:
        def __init__(self, task, extraction_backend):
            self._task = task
            self.name = task.name
            self._extraction_backend = extraction_backend
            
        def iterate_models(self):
            for model_name in self._extraction_backend._model_namespace.iter_module_names():
                model = self._extraction_backend._model_namespace.instantiate_plugin(model_name)
                try:
                    model.get_task_implementation(self.name)
                except MissingTaskImplementationException:
                    continue
                yield ExtractionBackend.ModelInterface(model = model, extraction_backend=self._extraction_backend)
        
        def get_input_schema(self):
            return self._task.get_input_schema()
        
        def get_output_schema(self):
            return self._task.get_output_schema()
    
    def __init__(self, job_builder, result_check_interval, task_namespace, model_namespace, default_task, default_models, service_manager):
        self._job_builder = job_builder
        self._result_check_interval = result_check_interval
        self._task_namespace = task_namespace
        self._model_namespace = model_namespace
        self.default_task = default_task
        self.default_models = default_models
        self._service_manager = service_manager
        
    def _apply_defaults(self, model_name, task_name):
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
    
    def create_job(self, model_name = None, task_name = None, kwargs = {}):
        model_name, task_name = self._apply_defaults(model_name, task_name)
        
        job = self._job_builder.from_task_and_model_name(task_name, model_name, kwargs)
        
        return ExtractionBackend.JobInterface(job=job, result_check_interval=self._result_check_interval)
    
    def get_model(self, task_name=None, model_name=None):
        if model_name is None:
            model_name, _ = self._apply_defaults(task_name=task_name, model_name=model_name)
        model = self._model_namespace.instantiate_plugin(model_name)
        return ExtractionBackend.ModelInterface(model=model, extraction_backend=self)
    
    def get_task(self, task_name = None):
        if task_name is None:
            _, task_name = self._apply_defaults(None, task_name)
        task = self._task_namespace.instantiate_plugin(task_name)
        return ExtractionBackend.TaskInterface(task=task, extraction_backend=self)
    
    def iterate_tasks(self):
        for task_name in self._task_namespace.iter_module_names():
            yield ExtractionBackend.TaskInterface(task = self._task_namespace.instantiate_plugin(task_name), extraction_backend = self)
    
    def iterate_models(self):
        for model_name in self._model_namespace.iter_module_names():
            yield ExtractionBackend.ModelInterface(model=self._model_namespace.instantiate_plugin(model_name), extraction_backend=self)
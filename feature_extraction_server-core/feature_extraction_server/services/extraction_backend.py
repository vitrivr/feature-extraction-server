import logging
logger = logging.getLogger(__name__)

from feature_extraction_server.core.exceptions import MissingTaskImplementationException
from simple_plugin_manager.settings import FloatSetting
from simple_plugin_manager.service import Service
from simple_plugin_manager.services.settings_manager import SettingsManager
from feature_extraction_server.services.job_builder import JobBuilder
from feature_extraction_server.services.model_namespace import ModelNamespace
from feature_extraction_server.services.task_namespace import TaskNamespace



class ExtractionBackend(Service):
    
    @staticmethod
    def initialize_service(settings_manager : SettingsManager, model_namespace : ModelNamespace, task_namespace : TaskNamespace, job_builder : JobBuilder):
        logger.debug("Initializing ExtractionBackend")
        result_check_interval_setting = FloatSetting("RESULT_CHECK_INTERVAL", 0.1, "The interval in seconds between checks for the result of a job.")
        settings_manager.add_setting(result_check_interval_setting)
        
        return ExtractionBackend(
            job_builder=job_builder,
            task_namespace= task_namespace,
            model_namespace=model_namespace,
            result_check_interval=result_check_interval_setting.get()
        )
        
    class JobInterface:
        def __init__(self, job, result_check_interval):
            self._job = job
            self._result_check_interval = result_check_interval
            self.id = job.id
            
        
        def start(self):
            self._job.start()
        
        def get_state(self):
            return self._job.get_state()
        
        def get_result(self):
            return self._job.get_result(self._result_check_interval)
    
    class ModelInterface:
        def __init__(self, model, extraction_backend):
            self._model = model
            self.name = model.name
            self._extraction_backend = extraction_backend
        
        def iterate_tasks(self):
            for task_name in self._extraction_backend._task_namespace.iter_module_names():
                task = self._extraction_backend._task_namespace.instantiate_plugin(task_name)
                if not task.is_implemented(self._model):
                    continue
                yield ExtractionBackend.TaskInterface(task = self._extraction_backend._task_namespace.instantiate_plugin(task_name), extraction_backend = self._extraction_backend)
        
        def start(self):
            self._model.start()
        
        def stop(self):
            self._model.stop()
        
        def get_n_jobs(self):
            return self._model.get_n_jobs()
        
        def get_jobs(self):
            return self._model.get_jobs()

        def get_state(self):
            return self._model.get_state()
    
    class TaskInterface:
        def __init__(self, task, extraction_backend):
            self._task = task
            self.name = task.name
            self._extraction_backend = extraction_backend
            
        def iterate_models(self):
            for model_name in self._extraction_backend._model_namespace.iter_module_names():
                model = self._extraction_backend._model_namespace.instantiate_plugin(model_name)
                if not self._task.is_implemented(model):
                    continue
                yield ExtractionBackend.ModelInterface(model = model, extraction_backend=self._extraction_backend)
        
        def get_input_data_model(self):
            return self._task.get_input_data_model()
        
        def get_output_data_model(self):
            return self._task.get_output_data_model()
    
    def __init__(self, job_builder, result_check_interval, task_namespace, model_namespace):
        self._job_builder = job_builder
        self._result_check_interval = result_check_interval
        self._task_namespace = task_namespace
        self._model_namespace = model_namespace
    
    def create_job(self, model_name, task_name, batched, kwargs):
        
        job = self._job_builder.from_task_and_model_name(
            task_name=task_name, model_name=model_name, batched=batched, kwargs=kwargs)
        
        return ExtractionBackend.JobInterface(job=job, result_check_interval=self._result_check_interval)
    
    def get_model(self, model_name):
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
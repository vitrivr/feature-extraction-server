import logging
logger = logging.getLogger(__name__)

from feature_extraction_server.core.exceptions import NoDefaultTaskException, NoDefaultModelException

class ApplicationInterface:
    
    class JobInterface:
        def __init__(self, job, result_check_interval):
            self._job = job
            self._result_check_interval = result_check_interval
        
        def start(self):
            self._job.start()
        
        def get_result(self):
            return self._job.get_result(self._result_check_interval)
    
    class ModelInterface:
        def __init__(self, startable_model):
            self._model = startable_model
        
        def start(self):
            self._model.start()
        
        def stop(self):
            self._model.stop()
    
    def __init__(self, job_builder, startable_model_builder, result_check_interval, task_namespace, model_namespace, default_task, default_models):
        self._job_builder = job_builder
        self._startable_model_builder = startable_model_builder
        self._result_check_interval = result_check_interval
        self._task_namespace = task_namespace
        self._model_namespace = model_namespace
        self.default_task = default_task
        self.default_models = default_models
        
    def _apply_defaults(self, model_name, task_name):
        if task_name is None:
            task_name = self.default_task
            if task_name is None:
                error_msg = "task_name must be set if no default task is set."
                logger.warn(error_msg)
                raise NoDefaultTaskException(error_msg)
        if model_name is None:
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
        
        return ApplicationInterface.JobInterface(job, self._result_check_interval)
    
    def get_model(self, model_name = None, task_name = None):
        model_name, _ = self._apply_defaults(model_name, task_name)
        model = self._startable_model_builder.from_model_name(model_name)
        return ApplicationInterface.ModelInterface(model)
    
    def list_all_task_names(self):
        return self._task_namespace.iter_plugin_names()
    
    def list_all_model_names(self):
        return self._model_namespace.iter_plugin_names()
    
    def list_models_for_task(self, task_name):
        for model_name in self._model_namespace.iter_plugin_names():
            model_plugin = self._model_namespace.get_plugin(model_name)
            if hasattr(model_plugin, task_name):
                yield model_name
    
    def list_tasks_for_model(self, model_name):
        model_plugin = self._model_namespace.get_plugin(model_name)
        for task_name in self._task_namespace.iter_plugin_names():
            if hasattr(model_plugin, task_name):
                yield task_name
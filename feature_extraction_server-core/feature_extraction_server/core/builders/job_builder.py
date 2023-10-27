from feature_extraction_server.core.job import Job
# from feature_extraction_server.core.exceptions import NoDefaultModelException, NoDefaultTaskException
import logging
logger = logging.getLogger(__name__)

class JobBuilder:
    def __init__(self, model_builder, task_builder, execution_state):
        self.model_builder = model_builder
        self.task_builder = task_builder
        self.execution_state = execution_state
    
    def from_task_and_model_name(self, task_name, model_name, kwargs):
        model = self.model_builder.from_model_name(model_name)
        task = self.task_builder.from_task_and_model_name(task_name, model_name)
        return Job(task=task, model=model, kwargs=kwargs, execution_state=self.execution_state)
    
    # def from_task_name(self, task_name, kwargs):
    #     try:
    #         model_name = self.default_model_names[task_name]
    #     except KeyError:
    #         error_msg = f"Task {task_name} does not have a default model."
    #         logger.warn(error_msg)
    #         raise NoDefaultModelException(error_msg)
    #     return self.from_task_and_model_name(task_name, model_name, kwargs)
    
    # def from_defaults(self, kwargs):
    #     if self.default_task_name is None:
    #         error_msg = "No default task name is set."
    #         logger.warn(error_msg)
    #         raise NoDefaultTaskException(error_msg)
    #     return self.from_task_name(self.default_task_name, kwargs)
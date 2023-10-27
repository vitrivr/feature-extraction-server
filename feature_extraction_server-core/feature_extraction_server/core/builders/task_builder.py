from feature_extraction_server.core.task import Task
from feature_extraction_server.core.exceptions import TaskNotFoundException

class TaskBuilder:
    def __init__(self, model_namespace, task_namespace):
        self.model_namespace = model_namespace
        self.task_namespace = task_namespace
    
    def from_task_and_model_name(self, task_name, model_name):
        if not self.task_namespace.has_plugin(task_name):
            raise TaskNotFoundException(f"Task {task_name} is not a valid task.")
        
        plugin = self.task_namespace.get_plugin(task_name)
        return Task(task_name, plugin, self.model_namespace.get_plugin(model_name))
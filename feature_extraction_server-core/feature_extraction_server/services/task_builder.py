from feature_extraction_server.services.task_namespace import TaskNamespace
from feature_extraction_server.core.exceptions import TaskNotFoundException
from simple_plugin_manager.service import Service

class TaskBuilder(Service):
    @staticmethod
    def initialize_service(task_namespace : TaskNamespace):
        return TaskBuilder(task_namespace = task_namespace)
    
    def __init__(self, task_namespace):
        self.task_namespace = task_namespace
    
    def from_task_name(self, task_name):
        if not self.task_namespace.has_plugin(task_name):
            raise TaskNotFoundException(f"Task {task_name} is not a valid task.")
        
        return self.task_namespace.get_plugin(name = task_name)

from simple_plugin_manager.module_namespace import ModuleNamespace
from simple_plugin_manager.service_manager import ServiceManager


class TaskNamespace(ModuleNamespace):
    
    @staticmethod
    def initialize_service(service_manager: ServiceManager):
        from feature_extraction_server.core.task import Task
        return TaskNamespace("feature_extraction_server.tasks", super_type=Task, service_manager=service_manager)
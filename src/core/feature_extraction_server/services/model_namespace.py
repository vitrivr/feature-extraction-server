
from simple_plugin_manager.module_namespace import ModuleNamespace
from simple_plugin_manager.service_manager import ServiceManager


class ModelNamespace(ModuleNamespace):
    
    @staticmethod
    def initialize_service(service_manager: ServiceManager):
        from feature_extraction_server.core.model import Model
        return ModelNamespace("feature_extraction_server.models", super_type=Model, service_manager=service_manager)
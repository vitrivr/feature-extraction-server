
from simple_plugin_manager.module_namespace import ModuleNamespace
from simple_plugin_manager.service_manager import ServiceManager

class ConsumerNamespace(ModuleNamespace):
    
    @staticmethod
    def initialize_service(service_manager: ServiceManager):
        from feature_extraction_server.core.consumer import Consumer
        return ConsumerNamespace("feature_extraction_server.consumers", super_type=Consumer, service_manager=service_manager)
from feature_extraction_server.core.namespace import PluginNamespace
from feature_extraction_server.core.task import Task
from feature_extraction_server.core.model import Model
from feature_extraction_server.core.consumer import Consumer
from feature_extraction_server.services.locator_service import Locator
from injector import Module, singleton, provider, Injector, threadlocal



class TaskNamespace(PluginNamespace):
    def __init__(self, locator : Locator):
        super().__init__("tasks",  super_type=Task, locator=locator)

class ModelNamespace(PluginNamespace):
    def __init__(self, locator : Locator):
        super().__init__("models", super_type=Model, locator=locator)

class ConsumerNamespace(PluginNamespace):
    def __init__(self, locator : Locator):
        super().__init__("consumers", super_type=Consumer, locator=locator)

class ServiceNamespace(PluginNamespace):
    def __init__(self, locator : Locator):
        super().__init__("services", super_type=Module, locator=locator)


class ServiceInjector(Injector):
    
    def __init__(self, services : ServiceNamespace):
    
        service_classes = []
        for service_name in services.iter_module_names():
            service_class = services.get_plugin_type(service_name)
            service_classes.append(service_class)
            
        super().__init__(service_classes)
        
        



class NamespaceService(Module):
    
    @singleton
    @provider
    def provide_task_namespace(self, locator : Locator) -> TaskNamespace:
        instance = TaskNamespace(locator=locator)
        locator.register_instance(TaskNamespace, instance)
        return instance
    
    @singleton
    @provider
    def provide_model_namespace(self, locator : Locator) -> ModelNamespace:
        instance = ModelNamespace(locator=locator)
        locator.register_instance(ModelNamespace, instance)
        return instance
    
    @singleton
    @provider
    def provide_consumer_namespace(self, locator : Locator) -> ConsumerNamespace:
        instance = ConsumerNamespace(locator=locator)
        locator.register_instance(ConsumerNamespace, instance)
        return instance
    
    @singleton
    @provider
    def provide_service_namespace(self, locator : Locator) -> ServiceNamespace:
        instance = ServiceNamespace(locator=locator)
        locator.register_instance(ServiceNamespace, instance)
        return instance
    
    # @singleton
    # @provider
    # def provide_service_injector(self, services : ServiceNamespace) -> ServiceInjector:
    #     return ServiceInjector(services=services)
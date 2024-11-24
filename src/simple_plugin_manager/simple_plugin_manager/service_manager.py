

from simple_plugin_manager.utils import can_call_with_kwargs, get_annotations_with_inheritance
from simple_plugin_manager.exceptions import InjectionException
from simple_plugin_manager.plugin import Plugin

class ServiceNotFoundException(Exception):
    pass

class ServiceManager:
    
    class Plugin(Plugin):

        service_type = None
        
        def build_service(self):
            pass
    
    def __init__(self):
        self.services = {ServiceManager: self}
        
    
    def copy(self):
        cp = ServiceManager.__new__(ServiceManager)
        cp.services = {**self.services}
        cp.services[ServiceManager] = cp
        return cp
    
    def get_service(self, service_type, **kwargs):
        if self.has_service(service_type):
            return self.services[service_type]
        for service_plugin_type in ServiceManager.Plugin.get_implementations():
            if service_plugin_type.service_type is service_type:
                service_plugin = self.inject(service_plugin_type, **kwargs)
                break
        else:
            raise ServiceNotFoundException(f"Service not found {service_type}.")
        self.set_service(service_type, self.inject(service_plugin.build_service, **kwargs))
        return self.get_service(service_type)
    
    def set_service(self, service_type, instance) -> None :
        if service_type in self.services:
            raise Exception("Service already initialized.")
        if not isinstance(instance, service_type) or not issubclass(type(instance), service_type):
            raise Exception("Invalid instance.")
        self.services[service_type] = instance
    
    def has_service(self, service_type):
        return service_type in self.services
    
    def inject(self, func, **kwargs):
        annotations = dict(get_annotations_with_inheritance(func))
        for key, annotation in annotations.items():
            if not key in kwargs:
                try:
                    kwargs[key] = self.get_service(annotation, **kwargs)
                except ServiceNotFoundException:
                    pass
        if not can_call_with_kwargs(func, kwargs):
            raise InjectionException(f"Cannot inject {func.__name__} with {kwargs}")
        return func(**kwargs)


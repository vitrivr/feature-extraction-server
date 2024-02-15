

from functools import wraps
from simple_plugin_manager.service import Service
from simple_plugin_manager.utils import can_call_with_kwargs, get_annotations_with_inheritance
from simple_plugin_manager.exceptions import InjectionException


    

class ServiceManager:
    
    def __init__(self):
        self.injector_configs = []
        self.services = {ServiceManager: self}
    
    def get_service(self, service_type, **kwargs):
        getter = ServiceGetter(self, service_type)
        return getter.get(**kwargs)
    
    def set_service(self, service_type, instance) -> None :
        if service_type in self.services:
            raise Exception("Service already initialized.")
        if not isinstance(instance, service_type):
            raise Exception("Invalid instance.")
        self.services[service_type] = instance
    
    def is_initialized(self, service_type):
        return service_type in self.services
    
    # def configure_injector(self, service_type: type[Service]):
    #     def configure(binder):
    #         getter = ServiceGetter(self, service_type)
    #         binder.bind(service_type, to=injector.CallableProvider(getter.get))
    #     return configure
    
    def entrypoint(self, service_namespace):
        
        from simple_plugin_manager.services.service_namespace import ServiceNamespace
        from simple_plugin_manager.services.settings_manager import SettingsManager
        from simple_plugin_manager.services.synchronization_provider import SynchronizationProvider
        
        services = [ServiceNamespace, SettingsManager, SynchronizationProvider]
        
        for service_module_name in service_namespace.iter_module_names():
            main_type = service_namespace.get_module(service_module_name).get_main_type()
            services.append(main_type)
        
            
        #inj = injector.Injector([self.configure_injector(service) for service in services])
        
        initialized_services = 0
        while initialized_services != len(services):
            old_initialized_services = initialized_services
            initialized_services = 0
            for service in services:
                if self.is_initialized(service):
                    initialized_services += 1
                    continue
                getter = ServiceGetter(self, service)
                try:
                    self.inject(getter.get)
                    initialized_services += 1
                except InjectionException as e:
                    continue
            if old_initialized_services == initialized_services:
                raise Exception("Circular dependency detected.")
        
        # for service in services:
        #     if not self.is_initialized(service):
        #         inj.get(service)
    
    def inject(self, func, **kwargs):
        annotations = dict(get_annotations_with_inheritance(func))
        for key, annotation in annotations.items():
            if annotation in self.services and not key in kwargs:
                kwargs[key] = self.services[annotation]
        if not can_call_with_kwargs(func, kwargs):
            raise InjectionException(f"Cannot inject {func.__name__} with {kwargs}")
        return func(**kwargs)


class ServiceGetter:
    def __init__(self, service_manager: ServiceManager, service_type: type[Service]):
        self.service_manager = service_manager
        self.service_type = service_type
        def get(**kwargs):
            if self.service_type in self.service_manager.services:
                return self.service_manager.services[self.service_type]
            
            service = self.service_type.initialize_service(**kwargs)
            self.service_manager.set_service(self.service_type, service)
            return service
        self.get = wraps(service_type.initialize_service)(get)
    
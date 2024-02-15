import importlib, pkgutil, logging
from simple_plugin_manager.exceptions import LoadModuleFailedException
from simple_plugin_manager.service import Service
from simple_plugin_manager.module import Module

logger = logging.getLogger(__name__)

def iter_namespace(ns_name):
    try:
        ns_pkg = importlib.import_module(ns_name)
    except ModuleNotFoundError:
        return []
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

class ModuleNamespace(Service):
    def __init__(self, path, super_type, service_manager):
        self.path = path
        self.super_type = super_type
        self.discovered_modules = {}
        self.service_manager = service_manager
        
        for _, name, _ in iter_namespace(self.path):
            module_name = name.split(".")[-1]
            try:
                module = Module(name, super_type=super_type)
                module.load()
                
            except LoadModuleFailedException:
                continue
            self.discovered_modules[module_name] = module
    
    def get_module(self, name):
        return self.discovered_modules[name]
    
    def iter_module_names(self):
        return self.discovered_modules.keys()
    
    def has_module(self, name):
        return name in self.discovered_modules
    
    def instantiate_plugin(self, name, **kwargs):
        module = self.get_module(name)
        return self.service_manager.inject(module.get_main_type(), **kwargs)
    

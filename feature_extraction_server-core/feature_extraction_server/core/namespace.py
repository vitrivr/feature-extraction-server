import pkgutil
import importlib
import logging


from feature_extraction_server.core.exceptions import LoadPluginFailedException
from feature_extraction_server.core.plugin_module import PluginModule
from injector import ClassAssistedBuilder

logger = logging.getLogger(__name__)

def iter_namespace(ns_name):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    ns_pkg = importlib.import_module(ns_name)
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

class PluginNamespace:
    def __init__(self, path, super_type, locator):
        self.path = path
        self.super_type = super_type
        self.locator = locator
        
        self.discovered_modules = {}
        
        for _, name, _ in iter_namespace(f"feature_extraction_server.{self.path}"):
            module_name = name.split(".")[-1]
            try:
                module = PluginModule(name, super_type=super_type, locator=locator)
                
            except LoadPluginFailedException:
                continue
            self.discovered_modules[module_name] = module
            
    def get_plugin_type(self, name):
        return self.discovered_modules[name].main_type
    
    def get_plugin_module(self, name):
        return self.discovered_modules[name]
    
    def iter_module_names(self):
        return self.discovered_modules.keys()
    
    def has_plugin(self, name):
        return name in self.discovered_modules
    
    def instantiate_plugin(self, name, **kwargs):
        return self.get_plugin_module(name).instantiate_plugin(**kwargs)
    


# class InstantiablePluginNamespace(PluginNamespace):
#     def __init__(self, path, super_type, service_registry):
#         super().__init__(path, super_type)
#         self.service_registry = service_registry
    
#     def instantiate_plugin(self, name, **kwargs):
#         module = self.get_plugin_module(name)
#         builder = self.service_injector.get(ClassAssistedBuilder[module.main_type])
#         return builder.build(**kwargs)
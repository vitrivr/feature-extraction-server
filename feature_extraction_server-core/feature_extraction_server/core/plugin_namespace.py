# import pkgutil
# import importlib
# import logging
# from feature_extraction_server.core.plugin import Plugin

# logger = logging.getLogger(__name__)

# def iter_namespace(ns_name):
#     # Specifying the second argument (prefix) to iter_modules makes the
#     # returned name an absolute name instead of a relative one. This allows
#     # import_module to work without having to do additional modification to
#     # the name.
#     ns_pkg = importlib.import_module(ns_name)
#     return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

# class PluginNamespace:
#     def __init__(self, path, expected_globals):
#         self.path = path
        
#         self.discovered_plugins = {}
        
#         for _, name, _ in iter_namespace(f"feature_extraction_server.{self.path}"):
#             module_name = name.split(".")[-1]
#             self.discovered_plugins[module_name] = Plugin(name, expected_globals=expected_globals)
    
#     def add_settings(self, settings_manager):
#         for plugin_name in self.discovered_plugins.keys():
#             plugin = self.discovered_plugins[plugin_name]
#             plugin.add_settings(settings_manager)
    
#     def get_plugin(self, name):
#         return self.discovered_plugins[name]
    
#     def iter_module_names(self):
#         return self.discovered_plugins.keys()

#     def has_plugin(self, name):
#         return name in self.discovered_plugins
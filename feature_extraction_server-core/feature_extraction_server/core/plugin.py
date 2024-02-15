# import importlib
# import logging

# from feature_extraction_server.core.exceptions import LoadPluginFailedException
# from feature_extraction_server.core.utils import convert_to_camel_case

# logger = logging.getLogger(__name__)

# class Plugin:
#     def __init__(self, full_path, expected_globals):
#         self.full_path = full_path
#         self.expected_globals = expected_globals
#         self.__setstate__(self.__getstate__())

    
#     def __getstate__(self):
#         return (self.full_path, self.expected_globals)
    
#     def __setstate__(self, state):
#         self.full_path, self.expected_globals = state
        
#         self.globals = []
#         try:
#             logger.debug(f"Loading plugin {self.full_path}.")
#             self.module = importlib.import_module(self.full_path)
#             for glob in self.expected_globals:
#                 if not hasattr(self.module, glob):
#                     continue
#                 self.__dict__[glob] = getattr(self.module, glob)
#                 self.globals.append(glob)
#             name = self.full_path.split(".")[-1]
#             camel_case = convert_to_camel_case(name)
#             if not hasattr(self.module, camel_case):
#                 return
#             self.main_type = getattr(self.module, camel_case)
#         except ImportError as e:
#             error_msg = f"Plugin {self.full_path} could not be loaded: " + str(e)
#             logger.error(error_msg)
#             raise LoadPluginFailedException(error_msg) from e
    
#     # def add_settings(self, settings_manager):
#     #     try:
#     #         self.module.add_settings(settings_manager)
#     #     except AttributeError:
#     #         error_msg = f"Plugin {self.full_path} does not have a method add_settings(). Assuming no settings."
#     #         logger.debug(error_msg)
    
#     # def __getattr__(self, name):
#     #     try:
#     #         return super().__getattr__(name)
#     #     except AttributeError:
#     #         try:
#     #             return getattr(self.module, name)
#     #         except:
#     #             msg = f"Plugin {self.full_path} does not have a {name} attribute."
#     #             logger.debug(msg)
#     #             raise AttributeError(msg)


import importlib, logging
logger = logging.getLogger(__name__)
from simple_plugin_manager.exceptions import LoadModuleFailedException
from simple_plugin_manager.utils import convert_to_camel_case

class Module:
    
    def __init__(self, full_path, super_type):
        self.full_path = full_path
        self.super_type = super_type
    
    def __getstate__(self):
        return self.full_path, self.super_type
    
    def __setstate__(self, state):
        self.full_path, self.super_type = state
    
    def load(self):
        try:
            logger.debug(f"Loading plugin {self.full_path}.")
            self.module = importlib.import_module(self.full_path)
            name = self.full_path.split(".")[-1]
            camel_case = convert_to_camel_case(name)
            if not hasattr(self.module, camel_case):
                error_msg = f"Plugin {self.full_path} does not have a {camel_case} attribute."
                logger.error(error_msg)
                raise LoadModuleFailedException(error_msg)
            main_type = getattr(self.module, camel_case)
            if not self.super_type is None and not issubclass(main_type, self.super_type):
                error_msg = f"Plugin {self.full_path} does not have a {camel_case} attribute that is a subclass of {self.super_type}."
                logger.error(error_msg)
                raise LoadModuleFailedException(error_msg)
            self.main_type = main_type
        except ImportError as e:
            error_msg = f"Plugin {self.full_path} could not be loaded: " + str(e)
            logger.error(error_msg)
            raise LoadModuleFailedException(error_msg) from e
    
    def is_loaded(self):
        return hasattr(self, "main_type")
    
    def get_main_type(self):
        if not self.is_loaded():
            self.load()
        return self.main_type
    
    def get_attribute(self, name):
        if not self.is_loaded():
            self.load()
        return getattr(self.module, name)
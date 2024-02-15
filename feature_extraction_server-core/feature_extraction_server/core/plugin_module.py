import importlib
import logging

from injector import ClassAssistedBuilder

from feature_extraction_server.core.exceptions import LoadPluginFailedException
from feature_extraction_server.core.utils import convert_to_camel_case

logger = logging.getLogger(__name__)

class PluginModule:
    def __init__(self, full_path, super_type, locator):
        self.full_path = full_path
        self.super_type = super_type
        self.locator = locator
        self.__setstate__(self.__getstate__())

    
    def __getstate__(self):
        return self.full_path, self.super_type, self.locator
    
    def __setstate__(self, state):
        self.full_path, self.super_type, self.locator = state
        
        self.globals = []
        try:
            logger.debug(f"Loading plugin {self.full_path}.")
            self.module = importlib.import_module(self.full_path)
            name = self.full_path.split(".")[-1]
            camel_case = convert_to_camel_case(name)
            if not hasattr(self.module, camel_case):
                error_msg = f"Plugin {self.full_path} does not have a {camel_case} attribute."
                logger.error(error_msg)
                raise LoadPluginFailedException(error_msg)
            main_type = getattr(self.module, camel_case)
            if not issubclass(main_type, self.super_type):
                error_msg = f"Plugin {self.full_path} does not have a {camel_case} attribute that is a subclass of {self.super_type}."
                logger.error(error_msg)
                raise LoadPluginFailedException(error_msg)
            self.main_type = main_type
        except ImportError as e:
            error_msg = f"Plugin {self.full_path} could not be loaded: " + str(e)
            logger.error(error_msg)
            raise LoadPluginFailedException(error_msg) from e
    
    def instantiate_plugin(self, **kwargs):
        return self.locator.inject(self.main_type, **kwargs)
    
    def setup_plugin(self):
        return self.locator.inject(self.main_type.setup)
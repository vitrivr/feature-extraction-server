import importlib
import logging

from feature_extraction_server.core.exceptions import LoadPluginFailedException

logger = logging.getLogger(__name__)

class Plugin:
    def __init__(self, full_path):
        self.full_path = full_path
        self.__setstate__(self.__getstate__())
    
    def __getstate__(self):
        return self.full_path
    
    def __setstate__(self, state):
        self.full_path = state
        try:
            logger.debug(f"Loading plugin {self.full_path}.")
            self.module = importlib.import_module(self.full_path)
        except ImportError as e:
            error_msg = f"Plugin {self.full_path} could not be loaded: " + str(e)
            logger.error(error_msg)
            raise LoadPluginFailedException(error_msg) from e
    
    def add_settings(self, settings_manager):
        try:
            self.module.add_settings(settings_manager)
        except AttributeError:
            error_msg = f"Plugin {self.full_path} does not have a method add_settings(). Assuming no settings."
            logger.warn(error_msg)
    
    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except AttributeError:
            try:
                return getattr(self.module, name)
            except:
                error_msg = f"Plugin {self.full_path} does not have a {name} attribute."
                logger.warning(error_msg)
                raise AttributeError(error_msg)



from feature_extraction_server.core.exceptions import ModelNotFoundException
from feature_extraction_server.services.model_namespace import ModelNamespace
import logging
from simple_plugin_manager.service import Service
logger = logging.getLogger(__name__)

class ModelBuilder(Service):
    @staticmethod
    def initialize_service(model_namespace : ModelNamespace):
        logger.debug("Initializing ModelBuilder")
        return ModelBuilder(model_namespace = model_namespace)
    
    def __init__(self, model_namespace):
        self.model_namespace = model_namespace
    
    def from_model_name(self, name):
        if not self.model_namespace.has_plugin(name):
            error_msg = f"Model {name} not found."
            logger.error(error_msg)
            raise ModelNotFoundException(error_msg)
        
        return self.model_namespace.get_plugin(name=name)
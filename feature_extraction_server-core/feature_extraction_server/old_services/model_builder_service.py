from injector import Module, singleton, provider
from feature_extraction_server.core.builders.model_builder import ModelBuilder
from feature_extraction_server.services.namespace_service import ModelNamespace, ServiceInjector
from feature_extraction_server.core.execution_state import ExecutionState

import logging
logger = logging.getLogger(__name__)

class ModelBuilderService(Module):
    
    @singleton
    @provider
    def provide_model_builder(self, model_namespace : ModelNamespace) -> ModelBuilder:
        logger.debug("Initializing ModelBuilder")
        return ModelBuilder(model_namespace=model_namespace)
    

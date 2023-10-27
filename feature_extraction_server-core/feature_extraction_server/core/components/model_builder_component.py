from feature_extraction_server.core.components.component import Component
from feature_extraction_server.core.builders.model_builder import ModelBuilder
from feature_extraction_server.core.components.namespace_components import ModelNamespaceComponent
from feature_extraction_server.core.components.execution_state_component import ExecutionStateComponent

import logging
logger = logging.getLogger(__name__)

class ModelBuilderComponent(Component):
    
    @staticmethod
    def _init():
        logger.debug("Initializing ModelBuilder")
        return ModelBuilder(ModelNamespaceComponent.get(), ExecutionStateComponent.get())
    

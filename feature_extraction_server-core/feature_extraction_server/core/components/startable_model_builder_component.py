from feature_extraction_server.core.components.component import Component
from feature_extraction_server.core.components.namespace_components import ModelNamespaceComponent
from feature_extraction_server.core.components.execution_state_component import ExecutionStateComponent
from feature_extraction_server.core.builders.startable_model_builder import StartableModelBuilder
from feature_extraction_server.core.components.consumer_builder_component import ConsumerBuilderComponent

import logging
logger = logging.getLogger(__name__)

class StartableModelBuilderComponent(Component):
    
    @staticmethod
    def _init():
        logger.debug("Initializing StartableModelBuilder")
        return StartableModelBuilder(model_namespace=ModelNamespaceComponent.get(), execution_state=ExecutionStateComponent.get(), consumer_builder=ConsumerBuilderComponent.get())
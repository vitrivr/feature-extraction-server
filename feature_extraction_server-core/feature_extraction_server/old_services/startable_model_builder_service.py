
from feature_extraction_server.core.builders.startable_model_builder import StartableModelBuilder
from feature_extraction_server.services.namespace_service import ModelNamespace
from feature_extraction_server.core.execution_state import ExecutionState
from feature_extraction_server.core.builders.consumer_builder import ConsumerBuilder
from injector import Module, singleton, provider

import logging
logger = logging.getLogger(__name__)

# class StartableModelBuilderService(Module):
    
#     @singleton
#     @provider
#     def provide_startable_model_builder(self, model_namespace : ModelNamespace, execution_state : ExecutionState, consumer_builder : ConsumerBuilder) -> StartableModelBuilder:
#         logger.debug("Initializing StartableModelBuilder")
#         return StartableModelBuilder(model_namespace=model_namespace, execution_state=execution_state, consumer_builder=consumer_builder)
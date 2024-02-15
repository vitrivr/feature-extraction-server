# from feature_extraction_server.core.startable_model import StartableModel
# from feature_extraction_server.core.exceptions import ModelNotFoundException

# import logging
# logger = logging.getLogger(__name__)

# class StartableModelBuilder:
#     def __init__(self, model_namespace, execution_state, consumer_builder):
#         self.model_namespace = model_namespace
#         self.execution_state = execution_state
#         self.consumer_builder = consumer_builder
    
#     def from_model_name(self, name):
#         if not self.model_namespace.has_plugin(name):
#             error_msg = f"Model {name} not found."
#             logger.error(error_msg)
#             raise ModelNotFoundException(f"Model {name} not found.")
        
#         plugin = self.model_namespace.get_plugin(name)
#         return StartableModel(name, plugin, self.execution_state, self.consumer_builder)
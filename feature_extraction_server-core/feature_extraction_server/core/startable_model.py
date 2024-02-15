# from feature_extraction_server.core.model import Model
# from feature_extraction_server.core.exceptions import MissingConsumerTypeException
# import logging 
# logger = logging.getLogger(__name__)

# class StartableModel(Model):
#     def __init__(self, name, plugin, execution_state, consumer_builder):
#         super().__init__(name, plugin, execution_state)
#         self.consumer_builder = consumer_builder
    
#     def start(self):
#         logger.info(f"Starting model {self.name}")
#         self._state.set_starting()
#         model_consumer = None
#         try:
#             model_consumer_type_name = self.get_consumer_type_name()
#             model_consumer = self.consumer_builder.build(model_consumer_type_name, self)
#         except MissingConsumerTypeException as e :
#             error_msg = f"Model {self.name} does not have a consumer type. Using default consumer type"
#             logger.warning(error_msg)
#             model_consumer = self.consumer_builder.default(self)
            
#         model_consumer.start()
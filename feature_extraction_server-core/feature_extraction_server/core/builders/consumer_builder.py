from feature_extraction_server.core.consumer import Consumer
from feature_extraction_server.core.exceptions import InvalidConsumerTypeException
import logging 
logger = logging.getLogger(__name__)

class ConsumerBuilder:
    
    def __init__(self, default_consumer_type, consumer_namespace):
        self.default_consumer_type = default_consumer_type
        self.consumer_namespace = consumer_namespace
    
    def build(self, name, model):
        logger.debug(f"Building consumer of type {name} for model {model.name}")
        # if not self.consumer_namespace.has_plugin(name):
        #     error_msg = f"Consumer type {name} does not exist."
        #     logger.error(error_msg)
        #     raise InvalidConsumerTypeException(error_msg)
        return self.consumer_namespace.instantiate_plugin(name=name, model=model)
        
        
    def default(self, model):
        return self.build(self.default_consumer_type, model)
    


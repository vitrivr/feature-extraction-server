from simple_plugin_manager.settings import EnumSetting
from simple_plugin_manager.services.settings_manager import SettingsManager
from simple_plugin_manager.service_manager import ServiceManager
from simple_plugin_manager.service import Service
from feature_extraction_server.services.consumer_namespace import ConsumerNamespace
import logging 
logger = logging.getLogger(__name__)

class ConsumerBuilder(Service):
    
    @staticmethod
    def initialize_service(settings_manager: SettingsManager, service_manager: ServiceManager, consumer_namespace: ConsumerNamespace):
        logger.debug("Initializing ProcessBuilder")
        default_consumer_type_setting = EnumSetting("DEFAULT_CONSUMER_TYPE", "single_thread_consumer", list(consumer_namespace.iter_module_names()), "The default consumer type.")
        settings_manager.add_setting(default_consumer_type_setting)
        instance = ConsumerBuilder(
            default_consumer_type=default_consumer_type_setting.get(),
            consumer_namespace=consumer_namespace,
            service_manager=service_manager
            )
        return instance
    
    def __init__(self, default_consumer_type, consumer_namespace, service_manager):
        self.default_consumer_type = default_consumer_type
        self.consumer_namespace = consumer_namespace
        self.service_manager = service_manager
    
    def build(self, name, model):
        logger.debug(f"Building consumer of type {name} for model {model.name}")
        # if not self.consumer_namespace.has_plugin(name):
        #     error_msg = f"Consumer type {name} does not exist."
        #     logger.error(error_msg)
        #     raise InvalidConsumerTypeException(error_msg)
        return self.service_manager.inject(self.consumer_namespace.get_module(name).get_main_type(), model = model)
        
        
    def default(self, model):
        return self.build(self.default_consumer_type, model)
    


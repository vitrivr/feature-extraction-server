from feature_extraction_server.services.namespace_service import ConsumerNamespace
from feature_extraction_server.services.locator_service import Locator
from feature_extraction_server.core.settings import EnumSetting, SettingsManager
from feature_extraction_server.core.builders.consumer_builder import ConsumerBuilder
from injector import Module, singleton, provider

import logging
logger = logging.getLogger(__name__)

class ConsumerBuilderService(Module):
    
    @singleton
    @provider
    def provide_consumer_builder(self, consumer_namespace : ConsumerNamespace, settings_manager : SettingsManager, locator : Locator) -> ConsumerBuilder:
        logger.debug("Initializing ProcessBuilder")
        default_consumer_type_setting = EnumSetting("DEFAULT_CONSUMER_TYPE", "single_thread_consumer", list(consumer_namespace.iter_module_names()), "The default consumer type.")
        settings_manager.add_setting(default_consumer_type_setting)
        instance = ConsumerBuilder(
            default_consumer_type=default_consumer_type_setting.get(),
            consumer_namespace=consumer_namespace
            )
        locator.register_instance(ConsumerBuilder, instance)
        return instance
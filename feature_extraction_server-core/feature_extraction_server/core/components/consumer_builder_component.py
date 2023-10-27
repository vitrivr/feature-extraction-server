from feature_extraction_server.core.components.component import Component
from feature_extraction_server.core.components.log_server_component import LogServerComponent
from feature_extraction_server.core.components.settings_manager_component import SettingsManagerComponent
from feature_extraction_server.core.components.namespace_components import ConsumerNamespaceComponent
from feature_extraction_server.core.settings import EnumSetting
from feature_extraction_server.core.builders.consumer_builder import ConsumerBuilder

import logging
logger = logging.getLogger(__name__)

class ConsumerBuilderComponent(Component):
    
    @staticmethod
    def _init():
        logger.debug("Initializing ProcessBuilder")
        consumer_namespace = ConsumerNamespaceComponent.get()
        settings_manager = SettingsManagerComponent.get()
        default_consumer_type_setting = EnumSetting("DEFAULT_CONSUMER_TYPE", "single_thread_consumer", list(consumer_namespace.iter_plugin_names()), "The default consumer type.")
        settings_manager.add_setting(default_consumer_type_setting)
        return ConsumerBuilder(
            log_server = LogServerComponent.get(), 
            default_consumer_type=default_consumer_type_setting.get(),
            consumer_namespace=consumer_namespace
            )
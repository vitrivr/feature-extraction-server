from feature_extraction_server.core.components.component import Component
from feature_extraction_server.core.plugin_namespace import PluginNamespace

import logging
logger = logging.getLogger(__name__)

class TaskNamespaceComponent(Component):
        
    @staticmethod
    def _init():
        logger.debug("Initializing PluginNamespace 'tasks'")
        return PluginNamespace("tasks")
            

class ModelNamespaceComponent(Component):
    
    @staticmethod
    def _init():
        logger.debug("Initializing PluginNamespace 'models'")
        return PluginNamespace("models")

class ApiNamespaceComponent(Component):
    
    @staticmethod
    def _init():
        logger.debug("Initializing PluginNamespace 'apis'")
        return PluginNamespace("apis")

class ConsumerNamespaceComponent(Component):
        
    @staticmethod
    def _init():
        logger.debug("Initializing PluginNamespace 'consumers'")
        return PluginNamespace("consumers")
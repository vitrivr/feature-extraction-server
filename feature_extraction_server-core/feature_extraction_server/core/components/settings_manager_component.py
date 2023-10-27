from feature_extraction_server.core.components.component import Component
from feature_extraction_server.core.settings import SettingsManager

import logging
logger = logging.getLogger(__name__)


class SettingsManagerComponent(Component):
    
    @staticmethod
    def _init():
        logger.debug("Initializing SettingsManager")
        return SettingsManager()

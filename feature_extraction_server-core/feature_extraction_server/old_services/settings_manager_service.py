from injector import Module, provider, singleton

from feature_extraction_server.core.settings import SettingsManager
from feature_extraction_server.services.locator_service import Locator

class SettingsManagerService(Module):
    
    @singleton
    @provider
    def provide_settings_manager(self, locator : Locator) -> SettingsManager:
        instance = SettingsManager()
        locator.register_instance(SettingsManager, instance)
        return instance

from simple_plugin_manager.module_namespace import ModuleNamespace
from simple_plugin_manager.service import Service
from simple_plugin_manager.services.settings_manager import SettingsManager
from simple_plugin_manager.settings import StringSetting
from simple_plugin_manager.service_manager import ServiceManager


class ServiceNamespace(ModuleNamespace):
    
    @staticmethod
    def initialize_service(settings_manager : SettingsManager, service_manager : ServiceManager):
        service_namespace_name_setting = StringSetting("service_namespace", "services", "The name of the namespace where the services should be discovered.")
        #settings_manager.add_setting(service_namespace_name_setting)
        name = service_namespace_name_setting.get()
        return ServiceNamespace(name, Service, service_manager=service_manager)
    
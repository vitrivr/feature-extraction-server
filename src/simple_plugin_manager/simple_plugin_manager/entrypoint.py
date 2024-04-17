


from simple_plugin_manager.service_manager import ServiceManager
from simple_plugin_manager.services.service_namespace import ServiceNamespace
from simple_plugin_manager.services.settings_manager import SettingsManager


def entrypoint():
    servicemanager = ServiceManager()
    settingsmanager = servicemanager.get_service(SettingsManager)
    service_namespace_service = servicemanager.get_service(ServiceNamespace, settings_manager=settingsmanager, service_manager=servicemanager)
    servicemanager.entrypoint(service_namespace_service)
    return servicemanager
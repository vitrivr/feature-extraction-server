from simple_plugin_manager.service_manager import ServiceManager
import multiprocessing as mp
from simple_plugin_manager.plugin import register_plugin
import multiprocessing.managers as mp_managers

@register_plugin
class SynchronizationProvider(ServiceManager.Plugin):
    
    service_type = mp_managers.SyncManager
    
    def build_service(self):
        return mp.Manager()
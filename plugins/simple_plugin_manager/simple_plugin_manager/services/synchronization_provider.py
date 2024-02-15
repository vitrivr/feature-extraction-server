import multiprocessing as mp

from simple_plugin_manager.service import Service

class SynchronizationProvider(Service):
    
    def __init__(self):
        self.mp_manager = mp.Manager()
    
    def __getstate__(self) -> object:
        return
    
    def __setstate__(self, state) -> None:
        return
    
    def get_mp_manager(self):
        return self.mp_manager
    
    @staticmethod
    def initialize_service():
        return SynchronizationProvider()
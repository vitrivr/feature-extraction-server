from fastapi import FastAPI
from fastapi.routing import APIRoute
from simple_plugin_manager.settings import StringSetting, IntegerSetting
import logging
from simple_plugin_manager.services.settings_manager import SettingsManager
from simple_plugin_manager.service import Service
import os
from simple_plugin_manager.entrypoint import entrypoint as spm_entrypoint
from feature_extraction_server.services.log_server import LogServer


class FastApiApp(Service):
    
    def __init__(self, spec_path):
        self.app = FastAPI(spec_path=spec_path)
    
    def __getstate__(self):
        return
    
    def __setstate__(self, state):
        return
    
    @staticmethod
    def initialize_service(settings_manager : SettingsManager):
        spec_path_setting = StringSetting(name='SPEC_ROUTE', default='/openapi.json', description='The route at which the openapi spec is generated.')
        settings_manager.add_setting(spec_path_setting)
        fast_api_service = FastApiApp(spec_path=spec_path_setting.get())
        fast_api_service.app.settings_manager = settings_manager
        return fast_api_service




def create_app(*args):
    os.environ['SERVICE_NAMESPACE'] = 'feature_extraction_server.services'
    service_manager = spm_entrypoint()
    service_manager.get_service(LogServer).configure_worker()
    return service_manager.get_service(FastApiApp).app

def run_app():
    os.environ['SERVICE_NAMESPACE'] = 'feature_extraction_server.services'
    service_manager = spm_entrypoint()
    service_manager.get_service(LogServer).configure_worker()
    app = service_manager.get_service(FastApiApp).app
    
    settings_manager = service_manager.get_service(SettingsManager)
    
    host_setting = StringSetting(name='HOST', default='localhost', description='The host to bind to.')
    port_setting = IntegerSetting(name='PORT', default=8888, description='The port to bind to.')
    
    settings_manager.add_setting(host_setting)
    settings_manager.add_setting(port_setting)
    
    host = host_setting.get()
    port = port_setting.get()
    
    settings_manager.show_help()
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    run_app()
from apiflask import APIFlask
from simple_plugin_manager.settings import StringSetting, IntegerSetting
from simple_plugin_manager.services.settings_manager import SettingsManager
from simple_plugin_manager.service_manager import ServiceManager
from simple_plugin_manager.service import Service



class FlaskApp(Service):
    
    def __init__(self, name, spec_path):
        self.app = APIFlask(name, spec_path=spec_path)
    
    def __getstate__(self):
        return
    
    def __setstate__(self, state):
        return
    
    @staticmethod
    def initialize_service(settings_manager : SettingsManager, service_manager : ServiceManager):
        spec_path_setting = StringSetting(name='SPEC_ROUTE_FAST_API', default='/openapi.json', description='The route at which the openapi spec is generated.')
        settings_manager.add_setting(spec_path_setting)
        flask_app = FlaskApp(name=__name__, spec_path=spec_path_setting.get())
        flask_app.app.service_manager = service_manager
        return flask_app

from simple_plugin_manager.entrypoint import entrypoint as spm_entrypoint
from feature_extraction_server.services.log_server import LogServer
from simple_plugin_manager.services.settings_manager import SettingsManager
import logging
import os

def create_app():
    os.environ['SERVICE_NAMESPACE'] = 'feature_extraction_server.services'
    service_manager = spm_entrypoint()
    service_manager.get_service(LogServer).configure_worker()
    return service_manager.get_service(FlaskApp).app

def run_app():
    os.environ['SERVICE_NAMESPACE'] = 'feature_extraction_server.services'
    service_manager = spm_entrypoint()
    service_manager.get_service(LogServer).configure_worker()
    flask_app = service_manager.get_service(FlaskApp).app
    
    settings_manager = service_manager.get_service(SettingsManager)
    hostsetting = StringSetting("HOST", default="localhost", description="The host to run the server on.")
    portsetting = IntegerSetting("PORT", default=5000, description="The port to run the server on.")
    settings_manager.add_setting(hostsetting)
    settings_manager.add_setting(portsetting)
    
    logger = logging.getLogger(__name__)
    logger.debug("Starting dev server")
    logger.info(f"Running dev server on {hostsetting.get()}:{portsetting.get()}")
    flask_app.run(host=hostsetting.get(), port=portsetting.get(), debug=True, use_reloader=False)
import sys
sys.path.append('./feature_extraction_server-core/') 
import os

for dir in os.listdir('./plugins/'):
    sys.path.append(f'./plugins/{dir}/')

from feature_extraction_server.core.components import LogServerComponent, SettingsManagerComponent
from feature_extraction_server.flask.flask_app_component import InitializedFlaskAppComponent
from feature_extraction_server.core.settings import StringSetting, IntegerSetting


import logging

if __name__ == '__main__':
    
    LogServerComponent.get().configure_worker()
    
    settings_manager = SettingsManagerComponent.get()
    hostsetting = StringSetting("HOST", default="localhost", description="The host to run the server on.")
    portsetting = IntegerSetting("PORT", default=5000, description="The port to run the server on.")
    settings_manager.add_setting(hostsetting)
    settings_manager.add_setting(portsetting)
    
    flask_app = InitializedFlaskAppComponent.get()
    
    logger = logging.getLogger(__name__)
    logger.debug("Starting dev server")
    logger.info(f"Running dev server on {hostsetting.get()}:{portsetting.get()}")
    flask_app.run(host=hostsetting.get(), port=portsetting.get(), debug=True, use_reloader=False)
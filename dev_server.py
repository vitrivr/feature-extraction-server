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
    settings_manager.add_setting(StringSetting("HOST", default="localhost", description="The host to run the server on."))
    settings_manager.add_setting(IntegerSetting("PORT", default=5000, description="The port to run the server on."))
    
    from werkzeug.serving import run_simple
    flask_app = InitializedFlaskAppComponent.get()
    
    conf = settings_manager.get_config()
    
    logger = logging.getLogger(__name__)
    logger.debug("Starting dev server")
    for key, val in vars(conf).items():
        logger.debug(f"{key}: {val}")
    logger.info(f"Running dev server on {conf.HOST}:{conf.PORT}")
    run_simple(conf.HOST, conf.PORT, flask_app)
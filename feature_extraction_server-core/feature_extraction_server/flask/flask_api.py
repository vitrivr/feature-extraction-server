class NoRoutesException(Exception):
    pass


import logging
logger = logging.getLogger(__name__)

class FlaskApi:
    
    def __init__(self, api_plugin):
        self.api_plugin = api_plugin
    
    def add_routes(self, application_interface, flask_app):
        if not hasattr(self.api_plugin, "add_routes"):
            error_msg = f"The api plugin {self.api_plugin.name} does not have a method add_routes()."
            logger.error(error_msg)
            raise NoRoutesException(error_msg)
        self.api_plugin.add_routes(application_interface, flask_app)
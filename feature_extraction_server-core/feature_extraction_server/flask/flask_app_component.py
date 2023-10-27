from feature_extraction_server.core.settings import StringSetting
from feature_extraction_server.core.components import Component, SettingsManagerComponent, ApiNamespaceComponent, ApplicationInterfaceComponent
from feature_extraction_server.flask.flask_api import FlaskApi
from flask import Flask

class FlaskAppComponent(Component):
        
    @staticmethod
    def _init():
        return Flask(__name__)




class InitializedFlaskAppComponent(Component):
        
    @staticmethod
    def _init():
        api_namespace = ApiNamespaceComponent.get()
        application_interface = ApplicationInterfaceComponent.get()
        flask_app = FlaskAppComponent.get()
        for api_plugin_name in api_namespace.iter_plugin_names():
            api_plugin = api_namespace.get_plugin(api_plugin_name)
            api = FlaskApi(api_plugin)
            api.add_routes(application_interface=application_interface, flask_app=flask_app)
        return flask_app
    
    
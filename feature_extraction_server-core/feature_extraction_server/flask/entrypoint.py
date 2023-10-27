from feature_extraction_server.flask.flask_app_component import InitializedFlaskAppComponent

def entrypoint():
    return InitializedFlaskAppComponent.get()
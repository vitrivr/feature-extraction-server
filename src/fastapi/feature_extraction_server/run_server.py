from feature_extraction_server.services.fast_api_app import run_app

def entrypoint():
    run_app()

if __name__ == '__main__':
    run_app()
import logging, os


def post_worker_init(worker):
    """
    Do something on worker initialization
    """
    from feature_extraction_server.services.log_server import LogServer
    try:
        worker.app.service_manager.get_service(LogServer).configure_worker()
    except Exception as e:
        logging.error(f"Error configuring worker: {e}")    
    try:
        worker.app.wsgi.service_manager.get_service(LogServer).configure_worker()
    except Exception as e:
        logging.error(f"Error configuring worker: {e}")
    
    print(worker.app.wsgi.__dict__)

# def post_fork(server, worker):
#     import feature_extraction_server.app as app
#     app.log_server.configure_worker()
#     print(server, worker)
    
# def worker_int(worker):
#     import feature_extraction_server.app as app
#     app.log_server.configure_worker()
#     print(worker)
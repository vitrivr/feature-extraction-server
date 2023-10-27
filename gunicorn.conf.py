import logging, os


def post_worker_init(worker):
    """
    Do something on worker initialization
    """
    import feature_extraction_server.core.components.log_server_component as log_server_component
    log_server_component.LogServerComponent.get().configure_worker()


# def post_fork(server, worker):
#     import feature_extraction_server.app as app
#     app.log_server.configure_worker()
#     print(server, worker)
    
# def worker_int(worker):
#     import feature_extraction_server.app as app
#     app.log_server.configure_worker()
#     print(worker)
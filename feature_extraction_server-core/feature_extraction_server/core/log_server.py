from multiprocessing import Queue, Process
import logging
import logging.handlers
import time
import os


class LoggingConfigurationException(Exception):
    pass

class LogServer:
    
    queue = None
    
    def __init__(self, level, path) -> None:
        self.queue = Queue()
        self.level = level
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
    def listener_process(self):
        baselogger = logging.getLogger("feature_extraction_server")
        baselogger.setLevel(self.level)
        
        file_handler = logging.handlers.RotatingFileHandler(self.path, 'a', 300, 10)
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(processName)-10s(%(process)s) %(name)s %(levelname)-8s %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        
        root = logging.getLogger()
        
        root.addHandler(file_handler)
        root.addHandler(stream_handler)
        
        log_server_logger = logging.getLogger("feature_extraction_server.log_server")
        log_server_logger.debug("Log server started")
        
        while True:
            while not self.queue.empty():
                record = self.queue.get()
                logger = logging.getLogger(record.name)
                logger.handle(record)
            time.sleep(0.2)
    
    def start_server(self):
        listener = Process(target=self.listener_process, args=(), name="LogServerProcess")
        listener.start()
    
    
    def is_configured(self):
        logger = logging.getLogger()
        if len(logger.handlers) != 1:
            return False
        
        if type(logger.handlers[0]) != logging.handlers.QueueHandler:
            return False
        
        return True
        
    
    # def get_logger(self, name):
    #     if not self.is_configured():
    #         self.configure_worker()
    #     return logging.getLogger(name)
    
    def configure_worker(self):
        try:
            h = logging.handlers.QueueHandler(self.queue)
            root = logging.getLogger()
            for handler in root.handlers[:]:
                root.removeHandler(handler)
            root.addHandler(h)
            
            baselogger = logging.getLogger("feature_extraction_server")
            baselogger.setLevel(self.level)
            
            logging.getLogger(__name__).debug("Configured worker")
        except Exception as e:
            error_msg = "Error occurred during logging configuration. Logging will likely not work correctly. " + str(e)
            print(error_msg)
            raise LoggingConfigurationException(error_msg) from e
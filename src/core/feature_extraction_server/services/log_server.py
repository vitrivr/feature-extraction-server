from multiprocessing import Queue, Process
import logging
import logging.handlers
import time
import os

from simple_plugin_manager.service import Service
from simple_plugin_manager.services.settings_manager import SettingsManager
from simple_plugin_manager.services.synchronization_provider import SynchronizationProvider
from simple_plugin_manager.settings import EnumSetting, StringSetting


class LoggingConfigurationException(Exception):
    pass

class LogServer(Service):
    
    @staticmethod
    def initialize_service(settings_manager:SettingsManager, synchronization_provider : SynchronizationProvider):
        log_level_setting = EnumSetting("LOG_LEVEL", "INFO", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], "The log level.")
        log_path_setting = StringSetting("LOG_PATH", "logs/log.txt", "The path to the log file.")
        settings_manager.add_setting(log_level_setting)
        settings_manager.add_setting(log_path_setting)
        log_server = LogServer(log_level_setting.get(), log_path_setting.get(), queue=synchronization_provider.get_mp_manager().Queue())
        
        log_server.start_server()
        
        return log_server
    
    def __init__(self, level, path, queue) -> None:
        self.queue = queue
        self.level = level
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
    
    def __getstate__(self) -> object:
        return self.__dict__
    
    def __setstate__(self, state) -> None:
        self.__dict__.update(state)
        
    def listener_process(self):
        baselogger = logging.getLogger("example_package")
        baselogger.setLevel(self.level)
        
        logging.getLogger('injector').setLevel(self.level)
        
        file_handler = logging.handlers.RotatingFileHandler(self.path, 'a', 300, 10)
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(processName)-10s(%(process)s) %(name)s %(levelname)-8s %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        
        root = logging.getLogger()
        
        root.addHandler(file_handler)
        root.addHandler(stream_handler)
        
        log_server_logger = logging.getLogger(__name__)
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
        
        if logger.handlers[0].queue != self.queue:
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
            
            root.setLevel(self.level)
            
            # baselogger = logging.getLogger(__name__)
            # baselogger.setLevel(self.level)
            
            logging.getLogger(__name__).debug("Configured worker")
        except Exception as e:
            error_msg = "Error occurred during logging configuration. Logging will likely not work correctly. " + str(e)
            print(error_msg)
            raise LoggingConfigurationException(error_msg) from e
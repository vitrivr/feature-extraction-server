from feature_extraction_server.core.consumer import Consumer
from feature_extraction_server.services.log_server import LogServer
import multiprocessing as mp
import threading

import logging
logger = logging.getLogger(__name__)

class MultiThreadConsumer(Consumer):
    def __init__(self, model, log_server : LogServer):
        super().__init__(model)
        self.log_server = log_server
    
    def start(self):
        self.process = mp.Process(target=MultiThreadConsumer._run, args=(self.model, self.log_server))
        self.process.start()
        self.monitor_thread = threading.Thread(target=self.monitor_process)
        self.monitor_thread.start()
        
    def monitor_process(self):
        while True:
            self.process.join(timeout=1)
            if self.process.is_alive():
                continue
            else:
                logger.error("Process terminated unexpectedly. Restarting...")
                self.process = mp.Process(target=MultiThreadConsumer._run, args=(self.model, self.log_server))
                self.process.start()
    
    def _run(model, log_server):
        log_server.configure_worker()
        model.load_model()
        for job in model.fetch_jobs():
            # run in new thread
            threading.Thread(target=job.run).start()
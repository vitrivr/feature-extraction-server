from feature_extraction_server.core.consumer import Consumer
from feature_extraction_server.services.log_server import LogServer
from injector import inject

class SingleThreadConsumer(Consumer):
    
    @inject
    def __init__(self, model, log_server : LogServer):
        super().__init__(model)
        self.log_server = log_server

    def start(self):
        import multiprocessing as mp
        process = mp.Process(target=SingleThreadConsumer._run, args=(self.model, self.log_server))
        process.start()
        return process

    @staticmethod
    def _run(model, log_server):
        log_server.configure_worker()
        model.load_model()
        for job in model.fetch_jobs():
            job.run()




import logging
from feature_extraction_server.core.exceptions import MissingConsumerTypeException, LoadModelFailedException, InvalidConsumerTypeException
from feature_extraction_server.core.execution_state import ExecutionState

logger = logging.getLogger(__name__)
            



class Model:

    
    def __init__(self, name, plugin, execution_state):
        self.name = name
        self.plugin = plugin
        self._state = ExecutionState.ModelState(self.name, execution_state)
    
    def add_job(self, job):
        logger.debug(f"Adding job {job.id} to model {self.name}")
        self._state.add_job(job)

    def get_consumer_type_name(self):
        logger.debug(f"Getting consumer type for model {self.name}")
        if not hasattr(self.plugin, "consumer_type"):
            error_msg = f"Model {self.name} does not have a configured consumer type."
            logger.warning(error_msg)
            raise MissingConsumerTypeException(error_msg)
        
        return self.plugin.consumer_type
        

    def load_model(self):
        logger.info(f"Loading model {self.name}")

        if not hasattr(self.plugin, "load_model"):
            error_msg = f"Cannot load the model {self.name} because the model has not implemented the load_model function."
            logger.error(error_msg)
            raise LoadModelFailedException(error_msg)
        
        try:
            self._state.set_loading()
            self.plugin.load_model()
        except Exception as e:
            error_msg = f"Cannot load the model {self.name} because of another exception: " + str(e)
            logger.error(error_msg)
            raise LoadModelFailedException(error_msg) from e
    
    def fetch_jobs(self):
        try:
            self._state.set_running()
            while(True):
                next_job = self._state.get_next_job()
                logger.debug(f"Model {self.name} fetched job {next_job.id}")
                yield next_job
                if self._state.get_state() == "stopped":
                    logger.info(f"Model {self.name} stopped")
                    break
        except Exception as e:
            logger.error(f"Model {self.name} failed with exception: " + str(e))
            self._state.set_failed(e)


    
    def stop(self):
        self._state.set_stopped()


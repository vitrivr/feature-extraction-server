
import logging

from injector import inject
from feature_extraction_server.core.exceptions import LoadModelFailedException,StartModelFailedException, MissingTaskImplementationException
from feature_extraction_server.services.execution_state import ExecutionState
from feature_extraction_server.services.consumer_builder import ConsumerBuilder
import abc
from feature_extraction_server.core.utils import convert_to_snake_case

logger = logging.getLogger(__name__)
            



class Model():

    consumer_type_name = None
    
    def __init__(self, execution_state : ExecutionState, consumer_builder : ConsumerBuilder):
        self.name = self.get_name()
        self.consumer_builder = consumer_builder
        self._state = ExecutionState.ModelState(self.name, execution_state)
    
    def __getstate__(self):
        return self.name, self.consumer_builder, self._state
    
    def __setstate__(self, state):
        self.name, self.consumer_builder, self._state = state
        
    
    def get_name(self):
        type_name = type(self).__name__
        return convert_to_snake_case(type_name)
        
    
    def get_task_implementation(self, task_name):
        if not hasattr(self, task_name):
            error_msg = f"Model {self.name} does not have a configured task implementation for task {task_name}."
            raise MissingTaskImplementationException(error_msg)
        
        return getattr(self, task_name)
    
    def add_job(self, job):
        logger.debug(f"Adding job {job.id} to model {self.name}")
        self._state.add_job(job)
        
    def start(self):
        logger.info(f"Starting model {self.name}")
        self._state.set_starting()
        try:
            model_consumer = None
            if self.consumer_type_name is None:
                model_consumer = self.consumer_builder.default(self)
            else:
                model_consumer = self.consumer_builder.build(self.consumer_type_name, self)
                
            model_consumer.start()
        except Exception as e:
            self._state.set_failed(e)
            error_msg = f"Cannot start model {self.name} because of another exception: " + str(e)
            logger.error(error_msg)
            raise StartModelFailedException(error_msg) from e

    # def get_consumer_type_name(self):
    #     logger.debug(f"Getting consumer type for model {self.name}")
    #     if not hasattr(self.plugin, "consumer_type"):
    #         error_msg = f"Model {self.name} does not have a configured consumer type."
    #         logger.warning(error_msg)
    #         raise MissingConsumerTypeException(error_msg)
        
    #     return self.plugin.consumer_type
        

    def load_model(self):
        logger.info(f"Loading model {self.name}")
        
        try:
            self._state.set_loading()
            self._load_model()
        except Exception as e:
            error_msg = f"Cannot load the model {self.name} because of another exception: " + str(e)
            logger.error(error_msg)
            raise LoadModelFailedException(error_msg) from e
    
    def _load_model(self):
        pass
    
    def fetch_jobs(self):
        try:
            self._state.set_running()
            while(True):
                next_job = self._state.get_next_job()
                if next_job is None:
                    self._state.set_stopped()
                    logger.info(f"Model {self.name} stopped")
                    break
                logger.debug(f"Model {self.name} fetched job {next_job.id}")
                next_job.model = self
                yield next_job
        except Exception as e:
            logger.error(f"Model {self.name} failed with exception: " + str(e))
            self._state.set_failed(e)

    
    def setup():
        pass

    
    def stop(self):
        self._state.add_job(None)


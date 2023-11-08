import uuid
from feature_extraction_server.core.exceptions import JobIncompleteException
from feature_extraction_server.core.execution_state import ExecutionState
import time
import logging

logger = logging.getLogger(__name__)

class Job:
    def __init__(self, task, model, kwargs, execution_state):
        self.task = task
        self.model = model
        self.kwargs = kwargs
        self.id = str(uuid.uuid4())
        self._state = ExecutionState.JobState(self.id, execution_state)
    
    def start(self):
        logger.debug(f"Job {self.id} starting")
        self._state.set_starting()
        self.model.add_job(self)
    
    def get_result(self, check_interval=0.1):
        while True:
            try:
                result = self._state.get_result()
                logger.debug(f"Job {self.id} completed")
                return result
            except JobIncompleteException:
                time.sleep(check_interval)
    
    def run(self): 
        logger.debug(f"Job {self.id} running")
        return self._state.wrap(self.task.get_function())(**self.kwargs)




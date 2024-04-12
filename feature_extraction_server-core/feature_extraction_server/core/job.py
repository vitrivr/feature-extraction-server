import uuid
from feature_extraction_server.core.exceptions import JobIncompleteException
from feature_extraction_server.core.execution_state import JobState
import time
import logging

logger = logging.getLogger(__name__)

class Job:
    def __init__(self, task, model, kwargs, execution_state, batched):
        from feature_extraction_server.services.execution_state import ExecutionState
        self.task = task
        self.model = model
        self.kwargs = kwargs
        self.id = str(uuid.uuid4())
        self._state = ExecutionState.JobState(self.id, execution_state)
        self.batched = batched
    
    def start(self):
        logger.debug(f"Job {self.id} starting")
        self._state.set_starting()
        self.model.add_job(self)
    
    def get_result(self):
        return self._state.get_result()
    
    def run(self): 
        logger.debug(f"Job {self.id} running")
        func = self.task.wrap_model(self.model, self.batched)
        return self._state.wrap(func)(self.kwargs)

    def get_state(self):
        return self._state.get_state()

    def reraise_exception(self):
        self.model.reraise_exception()
        if self._state.get_state() == JobState.failed:
            raise self._state.get_exception()

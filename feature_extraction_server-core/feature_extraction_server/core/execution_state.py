import multiprocessing as mp
import logging
from feature_extraction_server.core.exceptions import ModelAlreadyStartedException, JobIncompleteException, JobExecutionException


logger = logging.getLogger(__name__)
        


class ExecutionState:
    def __init__(self, mp_manager, model_names):
        self.job_queues = mp_manager.dict()
        self.job_state = mp_manager.dict()
        self.model_state = mp_manager.dict()
        self.lock = mp_manager.Lock()
        for model_name in model_names:
            self.model_state[model_name] = {"state": "uninitialized"}
            self.job_queues[model_name] = mp_manager.Queue()
    
    class ModelState:
        def __init__(self, model_name, execution_state):
            self.name = model_name
            self.execution_state = execution_state
        
        @property
        def _state(self):
            with self.execution_state.lock:
                return self.execution_state.model_state[self.name]

        @_state.setter
        def _state(self, value):
            with self.execution_state.lock:
                self.execution_state.model_state[self.name] = value        
        
        def get_state(self):
            return self._state["state"]
        
        def set_starting(self):
            with self.execution_state.lock:
                if self.execution_state.model_state[self.name]["state"] != "uninitialized":
                    error_msg = f"Cannot start model {self.name} because it has already been started."
                    logger.debug(error_msg)
                    raise ModelAlreadyStartedException(error_msg)
                self.execution_state.model_state[self.name] = {"state": "starting"}
        
        def set_loading(self):
            self._state = {"state": "loading"}
        
        def set_running(self):
            self._state = {"state": "running"}
        
        def set_stopped(self):
            self._state = {"state": "stopped"}
        
        def set_failed(self, exception):
            self._state = {"state": "failed", "exception": exception}
        
        def get_next_job(self):
            if self.get_state() == "uninitialized":
                error_msg = f"Cannot fetch the next job for the model {self.name} because it is in an uninitialized state."
                logger.error(error_msg)
            return self.execution_state.job_queues[self.name].get()
        
        def add_job(self, job):
            if self.get_state() == "uninitialized":
                error_msg = f"Cannot add the job {job.id} to the model {self.name} because the model is in an uninitialized state."
                logger.error(error_msg)
            self.execution_state.job_queues[self.name].put(job)
        
        
    class JobState:
        def __init__(self, id, execution_state):
            self.execution_state = execution_state
            self.id = id
        
        @property
        def _state(self):
            with self.execution_state.lock:
                return self.execution_state.job_state[self.id]

        @_state.setter
        def _state(self, value):
            with self.execution_state.lock:
                self.execution_state.job_state[self.id] = value
        
        def get_state(self):
            return self._state["state"]
        
        def get_result(self):
            state = self._state
            if "exception" in state:
                error_msg = f"Cannot get the result of job {self.id} ({state['state']}) because there was an exception: " + str(state["exception"])
                logging.error(error_msg)
                raise JobExecutionException(error_msg) from state["exception"]
            
            if not "result" in state:
                error_msg = f"Cannot get the result of job {self.id} ({state['state']})."
                raise JobIncompleteException(error_msg)
            
            return state["result"]
        
        def set_starting(self):
            self._state = {"state": "starting"}
        
        def set_running(self):
            self._state = {"state": "running"}
        
        def set_complete(self, result):
            self._state = {"state": "complete", "result": result}
        
        def set_failed(self, exception):
            self._state = {"state": "failed", "exception":exception}
        
        def wrap(self, func):
            
            def inner(*args, **kwargs):
                self.set_running()
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    self.set_failed(e)
                    return
                self.set_complete(result)
            
            return inner

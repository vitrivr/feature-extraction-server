from enum import Enum

class ModelState(Enum):
    loading = "loading"
    running = "running"
    stopped = "stopped"
    failed = "failed"
    uninitialized = "uninitialized"
    starting = "starting"
    
    def startable(self):
        return self in [ModelState.uninitialized, ModelState.stopped, ModelState.failed]

class JobState(Enum):
    starting = "starting"
    running = "running"
    complete = "complete"
    failed = "failed"
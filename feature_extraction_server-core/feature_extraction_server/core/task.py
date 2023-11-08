import logging

logger = logging.getLogger(__name__)

class Task:
    
    def __init__(self, name, task_plugin, model_plugin):
        self.name = name
        self.task_plugin = task_plugin
        self.model_plugin = model_plugin
    
    def get_function(self):
        logger.debug(f"Getting wrapper from task plugin {self.task_plugin.full_path}.")
        wrapper = self.task_plugin.wrap
        
        logger.debug(f"Getting function {self.name} from model plugin {self.model_plugin.full_path}.")
        task_func = getattr(self.model_plugin, self.name)
        return wrapper(task_func)



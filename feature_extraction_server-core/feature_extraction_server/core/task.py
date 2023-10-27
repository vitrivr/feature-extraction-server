class Task:
    
    def __init__(self, name, task_plugin, model_plugin):
        self.name = name
        self.task_plugin = task_plugin
        self.model_plugin = model_plugin
    
    def get_function(self):
        return self.task_plugin.wrap(getattr(self.model_plugin, self.name))



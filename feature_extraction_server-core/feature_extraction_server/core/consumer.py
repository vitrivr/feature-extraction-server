class Consumer:
    
    def __init__(self, plugin, model, log_server):
        self.plugin = plugin
        self.model = model
        self.log_server = log_server
    
    def start(self):
        return self.plugin.start(self.model, self.log_server)
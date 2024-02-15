class LoadPluginFailedException(Exception):
    pass

class LoadModelFailedException(Exception):
    pass

class StartModelFailedException(Exception):
    pass

class TaskNotFoundException(Exception):
    pass

class TaskNotImplementedException(Exception):
    pass

class TaskExecutionException(Exception):
    pass

class ModelAlreadyStartedException(Exception):
    pass

class JobIncompleteException(Exception):
    pass

class JobExecutionException(Exception):
    pass

class UninitializedModelException(Exception):
    pass

# class MissingConsumerTypeException(Exception):
#     pass

class InvalidConsumerTypeException(Exception):
    pass    

class MissingConfigurationException(Exception):
    pass

class InvalidConfigurationException(Exception):
    pass

class ComponentAlreadySetException(Exception):
    pass

class ModelNotFoundException(Exception):
    pass

class NoDefaultModelException(Exception):
    pass

class NoDefaultTaskException(Exception):
    pass

class MissingTaskImplementationException(Exception):
    pass

class InvalidServiceException(Exception):
    pass
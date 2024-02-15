from injector import Module, singleton, provider
from feature_extraction_server.core.builders.task_builder import TaskBuilder
from feature_extraction_server.services.namespace_service import ServiceInjector, TaskNamespace

import logging
logger = logging.getLogger(__name__)

class TaskBuilderService(Module):
    
    @singleton
    @provider
    def provide_task_builder(self, task_namespace : TaskNamespace) -> TaskBuilder:
        logger.debug("Initializing TaskBuilder")
        return TaskBuilder(task_namespace=task_namespace)
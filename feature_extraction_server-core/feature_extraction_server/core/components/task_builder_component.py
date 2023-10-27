from feature_extraction_server.core.components.component import Component
from feature_extraction_server.core.builders.task_builder import TaskBuilder
from feature_extraction_server.core.components.namespace_components import TaskNamespaceComponent, ModelNamespaceComponent

import logging
logger = logging.getLogger(__name__)

class TaskBuilderComponent(Component):
    
    @staticmethod
    def _init():
        logger.debug("Initializing TaskBuilder")
        return TaskBuilder(model_namespace=ModelNamespaceComponent.get(), task_namespace=TaskNamespaceComponent.get())
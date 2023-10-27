from feature_extraction_server.core.components.component import Component
from feature_extraction_server.core.execution_state import ExecutionState
from feature_extraction_server.core.components.namespace_components import ModelNamespaceComponent
import multiprocessing as mp

import logging
logger = logging.getLogger(__name__)

class ExecutionStateComponent(Component):
    
    @staticmethod
    def _init():
        logger.debug("Initializing ExecutionState")
        model_namespace = ModelNamespaceComponent.get()
        mp_manager = mp.Manager()
        return ExecutionState(mp_manager=mp_manager, model_names=list(model_namespace.iter_plugin_names()))
from feature_extraction_server.services.namespace_service import ModelNamespace
from feature_extraction_server.services.locator_service import Locator
from feature_extraction_server.core.execution_state import ExecutionState
import multiprocessing as mp
from injector import Module, provider, singleton

import logging
logger = logging.getLogger(__name__)


class ExecutionStateService(Module):
    
    @singleton
    @provider
    def provide_execution_state(self, model_namespace : ModelNamespace, locator : Locator, mp_manager : mp.Manager) -> ExecutionState:
        logger.debug("Initializing ExecutionState")
        e_s =  ExecutionState(mp_manager=mp_manager, model_names=list(model_namespace.iter_module_names()))
        locator.register_instance(ExecutionState, e_s)
        return e_s
    
    @singleton
    @provider
    def provide_mp_manager(self) -> mp.Manager:
        return mp.Manager()
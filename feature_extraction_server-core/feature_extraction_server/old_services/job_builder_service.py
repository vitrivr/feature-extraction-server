from injector import Module, singleton, provider
from feature_extraction_server.core.builders.job_builder import JobBuilder
from feature_extraction_server.services.namespace_service import ModelNamespace, TaskNamespace
from feature_extraction_server.core.execution_state import ExecutionState


import logging
logger = logging.getLogger(__name__)

class JobBuilderService(Module):
        
    @singleton
    @provider
    def provide_job_builder(self, model_namespace : ModelNamespace, task_namespace : TaskNamespace, execution_state : ExecutionState) -> JobBuilder:
        logger.debug("Initializing JobBuilder")

        
        return JobBuilder(model_namespace = model_namespace, task_namespace = task_namespace, execution_state = execution_state)
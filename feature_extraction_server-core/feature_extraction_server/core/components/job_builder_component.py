from feature_extraction_server.core.components.component import Component
from feature_extraction_server.core.builders.job_builder import JobBuilder
from feature_extraction_server.core.components.model_builder_component import ModelBuilderComponent
from feature_extraction_server.core.components.namespace_components import TaskNamespaceComponent, ModelNamespaceComponent
from feature_extraction_server.core.components.settings_manager_component import SettingsManagerComponent
from feature_extraction_server.core.components.task_builder_component import TaskBuilderComponent
from feature_extraction_server.core.components.execution_state_component import ExecutionStateComponent
from feature_extraction_server.core.settings import EnumSetting, NoValue, MissingConfigurationException


import logging
logger = logging.getLogger(__name__)

class JobBuilderComponent(Component):
        
    @staticmethod
    def _init():
        logger.debug("Initializing JobBuilder")

        
        return JobBuilder(ModelBuilderComponent.get(), TaskBuilderComponent.get(), ExecutionStateComponent.get())
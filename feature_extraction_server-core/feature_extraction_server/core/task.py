import logging
import abc
from feature_extraction_server.core.utils import convert_to_snake_case

logger = logging.getLogger(__name__)

class Task(abc.ABC):
    
    def __init__(self):
        self.name = self.get_name()
    
    def get_name(self):
        type_name = type(self).__name__
        return convert_to_snake_case(type_name)
    
    @abc.abstractmethod
    def wrap_implementation(self, implementation):
        pass
    
    @abc.abstractmethod
    def get_input_schema(self):
        pass
    
    @abc.abstractmethod
    def get_output_schema(self):
        pass
    
    
    def setup():
        pass

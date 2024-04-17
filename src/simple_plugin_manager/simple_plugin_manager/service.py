import abc
from typing import Any

class Service(abc.ABC):
    @abc.abstractmethod
    def initialize_service():
        pass
    
    # def __getstate__(self) -> object:
    #     return
    
    # def __setstate__(self, state) -> None:
    #     return
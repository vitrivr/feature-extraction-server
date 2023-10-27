import abc
from feature_extraction_server.core.exceptions import ComponentAlreadySetException

class Component(abc.ABC):
    _obj = None
    
    @classmethod
    def get(cls):
        if cls._obj is None:
            cls._obj = cls._init()
        return cls._obj
    
    @abc.abstractstaticmethod
    def _init():
        pass
    
    @classmethod
    def set(cls, obj):
        if cls._obj is not None:
            error_msg = f"Cannot set the component because it has already been set."
            raise ComponentAlreadySetException(error_msg)
        
        cls._obj = obj
    
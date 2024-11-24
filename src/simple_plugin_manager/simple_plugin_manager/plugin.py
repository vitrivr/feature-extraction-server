
from collections import defaultdict


def register_plugin(cls, b=None):
    if not hasattr(cls, "_registry"):
        cls._registry = defaultdict(list)
    if b is None:
        b = cls
    if b is object:
        return
    if not b is cls:
        cls._registry[b].append(cls)
    for base in b.__bases__:
        register_plugin(cls, base)
        
    return cls


class Plugin():
    
    _registry = defaultdict(list)
    
    @classmethod
    def get_implementations(cls):
        return cls._registry[cls]

from injector import Module, singleton, provider

import inspect

class Locator:
    def __init__(self):
        self.register = {}
    
    def register_instance(self, type, instance):
        self.register[type] = instance
    
    def inject(self, func, *args, **kwargs):
        sig = inspect.signature(func)
        parameters = sig.parameters

        for name, param in parameters.items():
            if name in kwargs:
                continue
            # Step 3: Inject instances
            param_type = param.annotation
            instance = self.register.get(param_type, None)
            if instance is not None:
                kwargs[name] = instance
            else:
                raise ValueError(f"No instance found for type {param_type}")

        # Step 4: Invoke the target function
        return func(*args, **kwargs)


class LocatorService(Module):
    
    @singleton
    @provider
    def provide_locator(self) -> Locator:
        return Locator()
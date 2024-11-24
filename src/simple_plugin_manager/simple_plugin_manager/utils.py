import inspect
import functools
import importlib, pkgutil

def convert_to_camel_case(s):
    # Split the string by underscore and capitalize each segment
    s = s.split('_')
    # Capitalize the first letter of each word and join them together
    return ''.join(word.capitalize() for word in s)

def convert_to_snake_case(s):

    # Convert from CamelCase to snake_case
    snake_case_name = ''.join(['_'+i.lower() if i.isupper() else i for i in s]).lstrip('_')

    return snake_case_name

def get_class_that_defined_method(meth):
    if isinstance(meth, functools.partial):
        return get_class_that_defined_method(meth.func)
    if inspect.ismethod(meth) or (inspect.isbuiltin(meth) and getattr(meth, '__self__', None) is not None and getattr(meth.__self__, '__class__', None)):
        for cls in inspect.getmro(meth.__self__.__class__):
            if meth.__name__ in cls.__dict__:
                return cls
        meth = getattr(meth, '__func__', meth)  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(inspect.getmodule(meth),
                      meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0],
                      None)
        if isinstance(cls, type):
            return cls
    return getattr(meth, '__objclass__', None)  # handle special descriptor objects

def get_annotations_with_inheritance(func):
    if inspect.isclass(func):
        func = func.__init__
    cls = get_class_that_defined_method(func)
    if cls is None:
        # Handle cases where func is not a method
        return func.__annotations__

    # Traverse the MRO to find the method in base classes
    for base_class in inspect.getmro(cls):
        if hasattr(base_class, func.__name__):
            method = getattr(base_class, func.__name__)
            break
    else:
        # Method not found in any base classes
        return {}

    # Retrieve and return annotations
    if inspect.isfunction(method) or inspect.ismethod(method):
        return {key:val.annotation for key, val in inspect.signature(method,eval_str=True).parameters.items() if not val.annotation is inspect.Parameter.empty}
    return {}

def can_call_with_kwargs(func, kwargs):
    sig = inspect.signature(func)
    parameters = sig.parameters

    for name, param in parameters.items():
        # Check for missing required arguments
        if param.default is inspect.Parameter.empty and name not in kwargs:
            return False

    rm_args = []
    # Check for extra arguments that the function does not accept
    for kw in kwargs:
        if kw not in parameters:
            rm_args.append(kw)
    for kw in rm_args:
        del kwargs[kw]

    return True

def import_all_modules_in_namespace(namespace):
        try:
            ns_pkg = importlib.import_module(namespace)
        except ModuleNotFoundError:
            return
        
        for module in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
            importlib.import_module(module.name)
            


# def myfunc(a: int, b: str) -> float:
#     return float(a)


# class MyClass:
#     def my_method(self, a: int, b: str) -> float:
#         return float(a)

# output = get_annotations_with_inheritance(myfunc)

# output2 = get_annotations_with_inheritance(MyClass.my_method)

# print(output)
from feature_extraction_server.core.dataformat import IImageFormat
from feature_extraction_server.core.datamodel import DataModel, Field
from feature_extraction_server.core.task import Task


class ChatCompletion(Task):
            
    input = DataModel("ChatCompletionInput",
                      Field("system_message", True, str, optional=True),
                      Field("user_message", True, str, optional=False),
                      Field("user_image", True, IImageFormat, optional=True),
                      Field("config", False, dict, optional=True),)
    
    output = DataModel("ChatCompletionOutput",
                       Field("assistant_message", True, str, optional=False))
            
        
        

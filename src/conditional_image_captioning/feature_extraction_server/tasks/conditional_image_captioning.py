from feature_extraction_server.core.dataformat import IImageFormat
from feature_extraction_server.core.datamodel import DataModel, Field
from feature_extraction_server.core.task import Task


class ConditionalImageCaptioning(Task):
            
    input = DataModel("ConditionalImageCaptioningInput",
                      Field("image", True, IImageFormat, optional=False),
                      Field("text", True, str, optional=False),
                      Field("config", False, dict, optional=True),)
    
    output = DataModel("ConditionalImageCaptioningOutput",
                       Field("caption", True, str, optional=False))
            
        
        

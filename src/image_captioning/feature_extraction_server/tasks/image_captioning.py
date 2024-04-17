from feature_extraction_server.core.dataformat import IImageFormat
from feature_extraction_server.core.datamodel import DataModel, Field
from feature_extraction_server.core.task import Task

class ImageCaptioning(Task):
            
        input = DataModel("ImageCaptioningInput",
                          Field("image", True, IImageFormat, optional=False),
                          Field("config", False, dict, optional=True),
                          )
        output = DataModel("ImageCaptioningOutput",
                           Field("caption", True, str, optional=False))
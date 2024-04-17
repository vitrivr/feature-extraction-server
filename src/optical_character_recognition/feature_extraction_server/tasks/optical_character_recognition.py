from feature_extraction_server.core.dataformat import IImageFormat
from feature_extraction_server.core.datamodel import DataModel, Field
from feature_extraction_server.core.task import Task

class OpticalCharacterRecognition(Task):
            
    input = DataModel("OpticalCharacterRecognitionInput",
                        Field("image", True, IImageFormat, optional=False),
                        Field("config", False, dict, optional=True),
                        )
    output = DataModel("OpticalCharacterRecognitionOutput",
                        Field("text", True, str, optional=False))
    
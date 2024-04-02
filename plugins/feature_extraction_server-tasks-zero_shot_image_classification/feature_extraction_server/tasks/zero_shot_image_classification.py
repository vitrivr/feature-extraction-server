from feature_extraction_server.core.dataformat import IImageFormat
from feature_extraction_server.core.datamodel import DataModel, Field
from feature_extraction_server.core.task import Task

from typing import List

class ZeroShotImageClassification(Task):
                
    input = DataModel("ZeroShotImageClassificationInput",
                        Field("image", True, IImageFormat, optional=False),
                        Field("classes", False, List[str], optional=True),
                        Field("config", False, dict, optional=True),
                        )
    
    output = DataModel("ZeroShotImageClassificationOutput",
                        Field("probabilities", True, List[float], optional=False),)
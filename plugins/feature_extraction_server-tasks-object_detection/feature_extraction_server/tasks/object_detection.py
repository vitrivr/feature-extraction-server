from feature_extraction_server.core.dataformat import IAudioFormat
from feature_extraction_server.core.datamodel import DataModel, Field
from feature_extraction_server.core.task import Task

from typing import List

    
class ObjectDetection(Task):
    input = DataModel("ObjectDetectionInput",
                        Field("image", True, IAudioFormat, optional=False),
                        Field("config", False, dict, optional=True),
                        )
    output = DataModel("ObjectDetectionOutput",
                        Field("labels", True, List[str], optional=False),
                        Field("boxes", True, List[List[int]], optional=False),
                        Field("scores", True, List[float], optional=False),
                        )
    

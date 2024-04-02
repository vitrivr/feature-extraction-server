from feature_extraction_server.core.dataformat import IImageFormat
from feature_extraction_server.core.datamodel import DataModel, Field
from feature_extraction_server.core.task import Task
from typing import List

class ImageEmbedding(Task):
        
    input = DataModel("ImageEmbeddingInput",
                    Field("image", True, IImageFormat, optional=False),
                    Field("config", False, dict, optional=True),
                    )
    output = DataModel("ImageEmbeddingOutput",
                          Field("embedding", True, List[float], optional=False))


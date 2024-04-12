from feature_extraction_server.core.datamodel import DataModel, Field
from feature_extraction_server.core.task import Task
from typing import List


class TextEmbedding(Task):
    input = DataModel("TextEmbeddingInput",
                      Field("text", True, str, optional=False),
                    Field("config", False, dict, optional=True),
                    )
    output = DataModel("TextEmbeddingOutput",
                        Field("embedding", True, List[float], optional=False),
                        )
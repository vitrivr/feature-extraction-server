from feature_extraction_server.core.datamodel import DataModel, Field
from feature_extraction_server.core.task import Task
from typing import List


class TextQueryEmbedding(Task):
    input = DataModel("TextQueryEmbeddingInput",
                      Field("query", True, str, optional=False),
                      Field("instruction", False, str, optional=False),
                    Field("config", False, dict, optional=True),
                    )
    output = DataModel("TextQueryEmbeddingOutput",
                        Field("embedding", True, List[float], optional=False),
                        )
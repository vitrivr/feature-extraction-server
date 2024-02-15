
from feature_extraction_server.core.task import Task
from feature_extraction_server.core.utils import prepare_text

from pydantic import BaseModel
from typing import Union, List

class InputSchema(BaseModel):
    text: Union[List[str], str]  

class OutputSchema(BaseModel):
    embedding: Union[List[List[float]], List[float]]  


class TextEmbedding(Task):

    
    def get_input_schema(self):
        return InputSchema
    
    def get_output_schema(self):
        return OutputSchema

    def wrap_implementation(self, func):
        def inner(text, config={}):
            text, return_list = prepare_text(text)
            result = func(text, config)
            if not return_list:
                result["embedding"] = result["embedding"][0]
            return {"embedding":result}
        return inner
from feature_extraction_server.core.utils import prepare_images

from feature_extraction_server.core.task import Task

from pydantic import BaseModel
from typing import Union, List

class InputSchema(BaseModel):
    image: Union[List[str], str]
    config: dict = {}

class OutputSchema(BaseModel):
    text: Union[List[str], str]

class OpticalCharacterRecognition(Task):
            
        def get_input_schema(self):
            return InputSchema
        
        def get_output_schema(self):
            return OutputSchema
        
        def wrap_implementation(self, func):
            def inner(image, config={}):
                image, return_list = prepare_images(image)
                result = func(image, config)
                if not return_list:
                    result["text"] = result["text"][0]
                return result
            return inner
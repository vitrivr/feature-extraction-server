from feature_extraction_server.core.utils import prepare_images
from feature_extraction_server.core.task import Task

from pydantic import BaseModel
from typing import Union, List

class InputSchema(BaseModel):
    image: Union[List[str], str]
    config: dict = {}

class OutputSchema(BaseModel):
    caption: Union[List[List[str]], List[str]]

class ImageCaptioning(Task):
            
        def get_input_schema(self):
            return InputSchema
        
        def get_output_schema(self):
            return OutputSchema
        def wrap_implementation(self, func):
            def inner(image, config={}):
                image, return_list = prepare_images(image)
                result = func(image, config)
                if not return_list:
                    result["caption"] = result["caption"][0]
                return result
            return inner
from feature_extraction_server.core.utils import prepare_images

from feature_extraction_server.core.task import Task

from pydantic import BaseModel
from typing import Union, List

class InputSchema(BaseModel):
    image: Union[List[str], str]
    classes: List[str]
    config: dict = {}

class OutputSchema(BaseModel):
    probabilities: Union[List[List[float]], List[float]]

class ZeroShotImageClassification(Task):
                
    def get_input_schema(self):
        return InputSchema
    
    def get_output_schema(self):
        return OutputSchema
    
    def wrap_implementation(self, func):
        def inner(image, classes, config ={}):
            image, return_list = prepare_images(image)
            result = func(image, classes, config)
            if not return_list:
                result["probabilities"] = result["probabilities"][0]
            return result
        return inner
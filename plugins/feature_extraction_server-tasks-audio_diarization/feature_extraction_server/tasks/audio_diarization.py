from feature_extraction_server.core.utils import prepare_audio
from feature_extraction_server.core.task import Task

from pydantic import BaseModel
from typing import Union, List

class InputSchema(BaseModel):
    audio: Union[List[str], str]  
    config: dict = {}


class AudioDiarization(Task):
            
        def get_input_schema(self):
            return InputSchema
        
        def get_output_schema(self):
            return str #todo: add output schema
        
        def wrap_implementation(self, func):
            def inner(audio, config={}):
                audio, return_list = prepare_audio(audio)
                result = func(audio, config)
                if not return_list:
                    result = result[0]
                return result
            return inner

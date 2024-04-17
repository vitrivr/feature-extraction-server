from feature_extraction_server.core.dataformat import IAudioFormat
from feature_extraction_server.core.datamodel import DataModel, Field
from feature_extraction_server.core.task import Task

class AutomatedSpeechRecognition(Task):
            
    input = DataModel("AutomatedSpeechRecognitionInput",
                        Field("audio", True, IAudioFormat, optional=False),
                        Field("config", False, dict, optional=True),
                        )
    
    output = DataModel("AutomatedSpeechRecognitionOutput",
                        Field("transcript", True, str, optional=False),
                        )
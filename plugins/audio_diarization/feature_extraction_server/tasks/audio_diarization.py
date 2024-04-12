from feature_extraction_server.core.dataformat import IAudioFormat
from feature_extraction_server.core.datamodel import DataModel, Field
from feature_extraction_server.core.task import Task


class AudioDiarization(Task):
    input = DataModel("AudioDiarizationInput",
                      Field("audio", True, IAudioFormat, optional=False),
                      Field("config", False, dict, optional=True),
                      )
    output = DataModel("AudioDiarizationOutput")
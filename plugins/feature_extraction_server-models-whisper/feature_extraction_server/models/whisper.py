from feature_extraction_server.core.model import Model

class Whisper(Model):

    def _load_model(self):
        global np
        import whisper
        import numpy as np

        self.model = whisper.load_model("base")
        

    def automated_speech_recognition(self, audio, config={}):
        audio_sample_array, _ = audio.resample(16000).to_numpy()
        
        output = self.model.transcribe(audio_sample_array.astype(np.float32),**config)
        return {"transcript":"".join([segment["text"] for segment in output["segments"]])}
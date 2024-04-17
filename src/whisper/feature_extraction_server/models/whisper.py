from feature_extraction_server.core.model import Model

class Whisper(Model):

    def _load_model(self):
        global np
        import whisper
        import numpy as np

        self.model = whisper.load_model("base")
        

    def automated_speech_recognition(self, audio, config={}):
        audio_segment = audio.to_pydub()
        if audio_segment.frame_rate != 16000: # 16 kHz
            audio_segment = audio_segment.set_frame_rate(16000)
        if audio_segment.sample_width != 2:   # int16
            audio_segment = audio_segment.set_sample_width(2)
        if audio_segment.channels != 1:       # mono
            audio_segment = audio_segment.set_channels(1)        
        arr = np.array(audio_segment.get_array_of_samples())
        arr = arr.astype(np.float32)/32768.0
        
        output = self.model.transcribe(arr,**config)
        return {"transcript":"".join([segment["text"] for segment in output["segments"]])}
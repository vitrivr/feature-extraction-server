from feature_extraction_server.core.model import Model

class Whisper(Model):

    def _load_model(self):
        global librosa, np
        import whisper
        import numpy as np
        import librosa

        self.model = whisper.load_model("base")
        

    def automated_speech_recognition(self, audio, config={}):
        audio_sample_array, audio_sampling_rate = audio.to_numpy()
        if audio_sample_array.ndim > 1:
            audio_sample_array = audio_sample_array.mean(axis=1)
        
        # resample the audio input to 16000Hz
        resampled = librosa.resample(audio_sample_array, orig_sr=audio_sampling_rate, target_sr=16000)
        
        output = self.model.transcribe(resampled.astype(np.float32),**config)
        return {"transcript":"".join([segment["text"] for segment in output["segments"]])}
from feature_extraction_server.core.model import Model
class Pyannote(Model):
    def _load_model(self):
        global pipeline
        from pyannote.audio import Pipeline
        self.pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token="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")

    def audio_diarization(self, audio, config={}):
        diarization = self.pipeline(audio.to_binary_stream())
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
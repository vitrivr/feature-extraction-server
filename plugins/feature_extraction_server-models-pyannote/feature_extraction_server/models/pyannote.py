
def load_model():
    global pipeline
    from pyannote.audio import Pipeline
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token="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")

def audio_diarization(audio, config={}):
    ret = []
    for a in audio:
        
        # 4. apply pretrained pipeline
        diarization = pipeline(a.to_binary_stream())

        # 5. print the result
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
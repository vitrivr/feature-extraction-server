def load_model():
    global librosa, np, model
    import whisper
    import numpy as np
    import librosa

    model = whisper.load_model("base")
    

def automated_speech_recognition(audio, config={}):
    audio = [a.to_numpy() for a in audio]
    results = []
    for audio_sample_array, audio_sampling_rate in audio:
        # if the audio is stereo, convert it to mono
        if audio_sample_array.ndim > 1:
            audio_sample_array = audio_sample_array.mean(axis=1)
        
        # resample the audio input to 16000Hz
        resampled = librosa.resample(audio_sample_array, orig_sr=audio_sampling_rate, target_sr=16000)
        
        output = model.transcribe(resampled.astype(np.float32),**config)
        results.append("".join([segment["text"] for segment in output["segments"]]))
    return results
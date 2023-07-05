from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa

# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-small")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
model.config.forced_decoder_ids = None



def automated_speech_recognition(audio, inference_args={}):
    rets = []
    
    for audio_sample_array, audio_sampling_rate in audio:
        
        # resample the audio input to 16000Hz
        resampled = librosa.resample(audio_sample_array, orig_sr=audio_sampling_rate, target_sr=16000)
        
        # preprocess the audio input
        input_features = processor(resampled, sampling_rate=16000, return_tensors="pt").input_features 

        # generate token ids
        predicted_ids = model.generate(input_features, **inference_args)
        # decode token ids to text

        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
        rets.append(transcription)

    return rets

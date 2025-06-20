import whisper
import os

model = whisper.load_model("base")  # Or "small", "medium", depending on accuracy/speed

def transcribe_audio(audio_path):
    try:
        print(f"🔍 Transcribing {audio_path}...")
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        print(f"❌ Error in transcription: {e}")
        return "Error transcribing audio."

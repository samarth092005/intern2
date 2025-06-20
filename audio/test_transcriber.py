# test_transcriber.py
from transcriber import transcribe_audio

file_path = "recordings/user_audio.wav"
text = transcribe_audio(file_path)
print("Final Output:\n", text)

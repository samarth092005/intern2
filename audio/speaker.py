import pyttsx3
import uuid
import os

def generate_speech(text, output_dir="static"):
    """
    Generates a speech audio file from text and saves it to static folder.
    Returns the filename.
    """
    engine = pyttsx3.init()
    filename = f"response_{uuid.uuid4().hex}.mp3"
    path = os.path.join(output_dir, filename)

    engine.save_to_file(text, path)
    engine.runAndWait()
    
    return filename

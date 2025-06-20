from flask import Blueprint, render_template, request, redirect, url_for, session
import os
import uuid

from ..transcriber import transcribe_audio
from ..predictor import predict_disorder  # or classify_text if you renamed it
from ..speaker import generate_speech  # optional: for text-to-speech audio
from flask import send_file
from ..report_generator import create_pdf  # Make sure this exists
from send_email import send_email_with_pdf


audio_bp = Blueprint("audio", __name__, template_folder="../templates")
UPLOAD_FOLDER = os.path.join(os.getcwd(), "recordings")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@audio_bp.route("/audio", methods=["GET"])
def audio_input():
    return render_template("audio.html")

@audio_bp.route("/audio/submit", methods=["POST"])
def audio_submit():
    if "audio" not in request.files:
        return "No audio file", 400

    file = request.files["audio"]
    if file.filename == "":
        return "No selected file", 400

    # Save the uploaded audio file
    audio_filename = f"user_audio.wav"
    audio_path = os.path.join(UPLOAD_FOLDER, audio_filename)
    file.save(audio_path)
    print(f"🎙️ Audio saved to: {audio_path}")

    # Step 1: Transcribe audio
    text = transcribe_audio(audio_path)

    # Step 2: Predict mental health disorder
    if text == "Error transcribing audio.":
        label, score = "Could not predict", 0
    else:
        label, score = predict_disorder(text)

    # Step 3: Generate speech response (optional)
    response_text = f"Prediction: {label}. Severity: {score}."
    audio_output_path = os.path.join("static", f"response_{uuid.uuid4().hex}.mp3")
    generate_speech(response_text, audio_output_path)

    # Step 4: Generate PDF report
    pdf_path = create_pdf(label, score, text)

    # Step 5: Send email with PDF and predefined message
    user_email = session.get("user_email")
    message = f"Dear User,\n\nBased on your audio assessment, the predicted disorder is {label} with a severity score of {score}%. Please find the attached report for more details.\n\nTake care,\nMed Nexus Team"
    if user_email:
        try:
            send_email_with_pdf(user_email, "Your Mental Health Audio Assessment Report", message, pdf_path)
        except Exception as e:
            import traceback
            print(f"Error sending email: {e}")
            traceback.print_exc()

    # Step 6: Pass everything to result page
    session["prediction"] = label
    session["severity"] = score
    session["transcript"] = text
    session["audio_path"] = audio_output_path

    return redirect(url_for("audio.audio_result"))

@audio_bp.route("/audio/result", methods=["GET"])
def audio_result():
    return render_template("audio_result.html",  # 🔄 changed this line
                           prediction=session.get("prediction"),
                           severity=session.get("severity"),
                           transcript=session.get("transcript"),
                           audio=session.get("audio_path"))

@audio_bp.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    label = session.get("prediction")
    severity = session.get("severity")
    transcript = session.get("transcript")

    pdf_path = create_pdf(label, severity, transcript)  # Create and return path
    return send_file(pdf_path, as_attachment=True)

# routes/result.py

from flask import Blueprint, render_template, request, session
from audio.predictor import predict_disorder
from send_email import send_email_with_pdf
from utils.pdf_generator import generate_pdf_report
import os


result_bp = Blueprint("result", __name__)

@result_bp.route("/result", methods=["POST"])
def result():
    # Get the combined user input
    binary_answers = request.form.getlist("binary_answers")
    text_answer = request.form.get("text_response")

    # Run prediction using ML model
    predicted_label, confidence = predict_disorder(text_answer)

    # Format a simple severity level
    if confidence >= 80:
        severity = "High"
    elif confidence >= 50:
        severity = "Moderate"
    else:
        severity = "Low"

    # Generate PDF report
    pdf_path = generate_pdf_report(predicted_label, severity, confidence, {"User Response": text_answer})

    # Compose email message
    message = f"Dear User,\n\nBased on your assessment, the predicted disorder is {predicted_label} with a severity level of {severity} ({confidence}%). Please find the attached report for more details.\n\nTake care,\nMed Nexus Team"

    # Send email if user email is available in session
    user_email = session.get("user_email")
    if user_email:
        try:
            send_email_with_pdf(user_email, "Your Mental Health Assessment Report", message, pdf_path)
        except Exception as e:
            import traceback
            print(f"Error sending email: {e}")
            traceback.print_exc()

    # Store result in session (optional)
    session["label"] = predicted_label
    session["confidence"] = confidence
    session["severity"] = severity
    session["user_text"] = text_answer

    return render_template("result.html",
                       result=predicted_label,
                       severity=severity,
                       score=confidence,
                       pdf_link=pdf_path)  # optional, if you use download link


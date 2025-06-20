from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import uuid
import os

def create_pdf(prediction, severity, transcript):
    filename = f"report_{uuid.uuid4().hex}.pdf"
    path = os.path.join("static", filename)

    c = canvas.Canvas(path, pagesize=letter)
    c.setFont("Helvetica", 14)
    c.drawString(100, 750, "🧠 Mental Health Detection Report")
    c.setFont("Helvetica", 12)
    c.drawString(100, 720, f"Prediction: {prediction}")
    c.drawString(100, 700, f"Severity: {severity}")
    c.drawString(100, 680, f"Transcribed Text:")
    text_obj = c.beginText(100, 660)
    text_obj.textLines(transcript)
    c.drawText(text_obj)
    c.showPage()
    c.save()

    return path

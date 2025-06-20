import uuid
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from data.disorder_info import disorder_details

def generate_pdf_report(disorder_name, severity_label, score, text_responses):
    info = disorder_details.get(disorder_name, {})
    file_id = str(uuid.uuid4())
    filename = f"static/reports/{file_id}.pdf"

    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(info.get("title", disorder_name), styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<b>Severity:</b> {severity_label} ({score}%)", styles["Normal"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"<b>Description:</b> {info.get('description', 'N/A')}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    if info.get("symptoms"):
        elements.append(Paragraph("<b>Symptoms:</b>", styles["Heading3"]))
        for s in info["symptoms"]:
            elements.append(Paragraph(f"• {s}", styles["Normal"]))
        elements.append(Spacer(1, 12))

    if info.get("causes"):
        elements.append(Paragraph(f"<b>Causes:</b> {info['causes']}", styles["Normal"]))
        elements.append(Spacer(1, 12))

    if info.get("treatment"):
        elements.append(Paragraph(f"<b>Treatment:</b> {info['treatment']}", styles["Normal"]))
        elements.append(Spacer(1, 12))

    if text_responses:
        elements.append(Paragraph("<b>User's Text Responses:</b>", styles["Heading3"]))
        for q, ans in text_responses.items():
            elements.append(Paragraph(f"<i>{q}</i>", styles["Normal"]))
            elements.append(Paragraph(f"{ans}", styles["Normal"]))
            elements.append(Spacer(1, 6))

    doc.build(elements)
    return filename

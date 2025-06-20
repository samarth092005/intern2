import smtplib
import os
from email.message import EmailMessage

def send_email_with_pdf(to_email, subject, body, pdf_path):
    from_email = "samarthagarwal.413@gmail.com"
    app_password = "anie bagk weit turhord"  # Replace this with your real app password

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(body)

    # Attach PDF
    with open(pdf_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(pdf_path)
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    # Send email via Gmail SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(from_email, app_password)
        smtp.send_message(msg)

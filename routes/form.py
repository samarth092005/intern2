from flask import Blueprint, render_template, request, redirect, url_for, session
from ml.predict import predict_disorder
from utils.pdf_generator import generate_pdf_report
import json

# Define Blueprint
form_bp = Blueprint('form', __name__)

# ✅ Load questions.json once at startup
with open("data/questions.json") as f:
    questions = json.load(f)

@form_bp.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Collect form responses
        responses = request.form.to_dict()

        # Predict disorder & severity
        prediction, severity = predict_disorder(responses)

        # Save to session (temporary memory)
        session['prediction'] = prediction
        session['severity'] = severity
        session['responses'] = responses

        return redirect(url_for('result.result_page'))

    # Render form with questions
    return render_template('form.html', questions=questions)

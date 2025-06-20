from flask import Blueprint, render_template, session, redirect, url_for

home_bp = Blueprint("home", __name__)

@home_bp.route('/home')  # 👈 yeh route ab '/home' pe chalega
def home():
    if 'username' not in session:
        return redirect(url_for('show_login'))  # ✅ correct endpoint name of login page
    return render_template("home.html")

@home_bp.route("/choose-input")
def choose_input():
    if 'username' not in session:
        return redirect(url_for('show_login'))  # ✅ same here
    return render_template("choose_input.html")

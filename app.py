from flask import Flask, render_template, request, redirect, url_for, session
from routes.home import home_bp
from routes.form import form_bp
from routes.result import result_bp
from audio.routes.audio import audio_bp

app = Flask(__name__)
app.secret_key = "abc123xyz987"  # Needed for sessions

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "audio"))


# Register Blueprints
app.register_blueprint(home_bp)
app.register_blueprint(form_bp)
app.register_blueprint(result_bp)
app.register_blueprint(audio_bp)

# 🔹 Show Login Page
@app.route('/')
def show_login():
    return render_template('login.html')


# 🔹 Login Handler
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    # Allow default user or user who just signed up
    if (username == 'user' and password == 'pass') or (
        username == session.get('username') and password == session.get('password')):
        
        session['username'] = username  # Store in session
        
        # ✅ THIS IS THE MAIN LINE YOU ASKED:
        return redirect(url_for('home.home'))  # home = blueprint name, home = function name inside home.py
        
    else:
        return render_template('login.html', error="Invalid username or password")

# 🔹 Signup Handler
@app.route('/signup', methods=['POST'])
def signup():
    session['username'] = request.form['newUsername']
    session['password'] = request.form['newPassword']
    return render_template('login.html', success="Account created successfully. Please log in.")

# 🔹 Store Email Route (keep existing)
@app.route("/store-email", methods=["POST"])
def store_email():
    data = request.get_json()
    session["user_email"] = data["email"]
    return "", 204

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('show_login'))

if __name__ == "__main__":
    print("✅ Flask server running at http://127.0.0.1:5000")
    app.run(debug=True)

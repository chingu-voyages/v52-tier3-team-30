from flask import Flask, redirect, render_template, request, make_response, session, abort, jsonify, url_for
from functools import wraps
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import timedelta
import os
from dotenv import load_dotenv

from utils import database

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configure session cookie settings
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Adjust session expiration as needed
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Can be 'Strict', 'Lax', or 'None'

# Firebase Admin SDK setup
cred = credentials.Certificate("firebase-auth.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user is authenticated
        if 'user' not in session:
            return redirect(url_for('login'))

        else:
            return f(*args, **kwargs)

    return decorated_function


@app.route('/auth', methods=['POST'])
def authorize():
    token = request.headers.get('Authorization')
    if not token or not token.startswith('Bearer '):
        return "Unauthorized", 401

    token = token[7:]  # Strip off 'Bearer ' to get the actual token

    try:
        decoded_token = auth.verify_id_token(token)  # Validate token here
        session['user'] = decoded_token  # Add user to session
        return redirect(url_for('dashboard'))

    except:
        return "Unauthorized", 401

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/form', methods=('GET', 'POST'))
def form():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        if 'request-form-submit' in request.form:
            name = request.form.get('inputName')
            email = request.form.get('inputEmail')
            phone = request.form.get('inputPhone')
            address = request.form.get('inputAddress')
            timeslot = request.form.get('inputTime')
            preferred_date = request.form.get('inputDate')
            resident_ref = database.create_resident(db, name, email, phone, address, timeslot, preferred_date)
            return render_template('form.html', msg='Form submitted successfully', requestId=resident_ref)
    return render_template('form.html')

@app.route('/status/<requestId>', methods=('GET', 'POST'))
def status(requestId):
    info = database.get_status(db, requestId)
    if info is None:
        return render_template('status.html', msg='Request ID: {} not found'.format(requestId))

    return render_template('status.html', msg='Request ID: {} found'.format(requestId), info=info)


@app.route('/login')
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove the user from session
    response = make_response(redirect(url_for('login')))
    response.set_cookie('session', '', expires=0)  # Optionally clear the session cookie
    return response


@app.route('/dashboard', methods=('GET', 'POST'))
@auth_required
def dashboard():
    data = database.get_all_requests(db)

    if request.method == 'POST':
        if 'mark-visited-submit' in request.form:
            requestId = request.form.get('mark-visited-submit')
            database.update_status(db, requestId, 'Visited')

    return render_template('dashboard.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
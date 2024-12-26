import os

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import firebase_admin
from firebase_admin import credentials, firestore

from utils.database import get_today_listings

script_directory = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_directory, "firebase-auth.json")

# Firebase Admin SDK setup
cred = credentials.Certificate(data_file)
firebase_admin.initialize_app(cred)
db = firestore.client()

sender_email = "admin@hlsolar.email"
STATUS_URL = "https://hlpractice.pythonanywhere.com/status/"

listings = get_today_listings(db)

def send_timeslot_email(receiver_email, name, id, timeslot):

    message = MIMEMultipart("alternative")
    message["Subject"] = f"[{id}] Solar Panel Confirmation Timeslot"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = f"""\
    Hi {name}!,
    Thank you for submitting a request for solar panel evaluation!
    Your confirmed timeslot is: {timeslot}
    Please visit this link to track your request status: {STATUS_URL}{id}
    """
    html = f"""\
    <html>
      <body>
        <p>Hi {name},<br>
           Thank you for submitting a request for solar panel evaluation!<br>
           Your confirmed timeslot is: {timeslot}<br>
           Please visit this <a href="{STATUS_URL}{id}" target="_blank">link</a> to track your request status.<br>      
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP("mail.smtpbucket.com", 8025) as server:
    #    server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

for key, item in listings.items():
    send_timeslot_email(item['email'], item['name'], key, item['timeslot'])
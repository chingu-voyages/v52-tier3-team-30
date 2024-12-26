import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


sender_email = "admin@hlsolar.email"
STATUS_URL = "https://hlpractice.pythonanywhere.com/status/"

def send_confirmation_email(receiver_email, name, id):

    message = MIMEMultipart("alternative")
    message["Subject"] = f"[{id}] Solar Panel Request Received"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = f"""\
    Hi {name}!,
    Thank you for submitting a request for solar panel evaluation!
    We have received for information.
    Please visit this link to track your request status: {STATUS_URL}{id}
    The confirmation timeslot will be sent to you via email, around midnight, on the day of the visit.
    """
    html = f"""\
    <html>
      <body>
        <p>Hi {name},<br>
           Thank you for submitting a request for solar panel evaluation!<br>
           We have received for information.<br>
           Please visit this <a href="{STATUS_URL}{id}">link</a> to track your request status.<br>      
           The confirmation timeslot will be sent to you via email, around midnight, on the day of the visit.
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
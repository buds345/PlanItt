# utils/email_sender.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER_EMAIL = "nesthub040@gmail.com"
SENDER_PASSWORD = "ayuk rpad jufv dlns"  # Use App Passwords for Gmail

def send_invite_email(to_email, guest_name, event_id, event_name, rsvp_url):
    subject = f"You're Invited to {event_name}!"
    body = f"""
    Hello {guest_name},

    You are invited to {event_name}!

    Please RSVP by clicking the link below:
    {rsvp_url}

    Thank you!
    """

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = SENDER_EMAIL
    message["To"] = to_email
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, message.as_string())
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

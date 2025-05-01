import smtplib
from email.message import EmailMessage

def send_verification_email(to_email, verification_link):
    msg = EmailMessage()
    msg["Subject"] = "Verify your email address"
    msg["From"] = "your-email@gmail.com"  # replace with your email
    msg["To"] = to_email
    msg.set_content(f"Click this link to verify your email: {verification_link}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("banelebanele938@gmail.com", "aqchitvwzzymkxvo")  # replace these
        smtp.send_message(msg)


import smtplib
import ssl
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(sender_email, sender_password, receiver_email, subject, message):
    # Set up the SMTP server
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587
    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Add the message body
    msg.attach(MIMEText(message, "plain"))


    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        # server.starttls(context=ssl.create_default_context())
        server.login(sender_email, sender_password)
        server.send_message(msg)


# Get command-line arguments
sender_email = sys.argv[1]
sender_password = sys.argv[2]
receiver_email = sys.argv[3]
subject = "Hello from Python"
message = "This is a test email sent using Python"


subject = "Hello"
message = "This is the email message."

send_email(sender_email, sender_password, receiver_email, subject, message)

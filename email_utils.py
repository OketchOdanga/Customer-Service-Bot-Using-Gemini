import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email_alert(to_email, department, message_body, customer_email):
    sender_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    subject = f"New Customer Request for {department} Department"
    body = f"""
    Hello {department} Team,

    A new customer request has been routed to your department.

    --- Message ---
    {message_body}

    --- Customer Email ---
    {customer_email}

    Please respond directly to the customer if needed.

    Regards,  
    AI Customer Service Agent
    """

    # Construct the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            print(f"[EMAIL SENT] to {to_email} for {department}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

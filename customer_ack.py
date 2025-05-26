import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_customer_acknowledgment(customer_email, department):
    sender_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    subject = "Acknowledgment: We've Received Your Request"
    body = f"""
    Hello,

    This is to confirm that your request has been received and forwarded to our {department} department.
    Our team is reviewing it and will get back to you shortly.

    Thank you for reaching out to us.

    Regards,
    AI Customer Service Agent
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = customer_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            print(f"[ACK EMAIL SENT] to customer: {customer_email}")
    except Exception as e:
        print(f"[ERROR] Failed to send acknowledgment email: {e}")

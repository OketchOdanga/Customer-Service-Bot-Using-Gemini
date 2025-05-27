# follow_up.py

import sqlite3
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

DB_NAME = "requests.db"
FOLLOW_UP_HOURS = 16 # Adjust as needed

def send_follow_up_email(customer_email, request_id):
    sender_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    subject = "Reminder: Your Support Request is Still Pending"
    body = f"""
    Hello,

    We're following up to let you know that your request (ID: {request_id}) is still being processed.
    We appreciate your patience and will get back to you as soon as possible.

    If you have additional information to share, feel free to reply to this email.

    Thank you for contacting us.

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
            print(f"[FOLLOW-UP SENT] to {customer_email} for request {request_id}")
    except Exception as e:
        print(f"[ERROR] Failed to send follow-up email: {e}")

def check_for_pending_requests():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cutoff_time = datetime.now() - timedelta(hours=FOLLOW_UP_HOURS)
    cutoff_str = cutoff_time.strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
        SELECT id, email, timestamp FROM requests
        WHERE status = 'Pending' AND timestamp <= ?
    ''', (cutoff_str,))

    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        request_id, email, _ = row
        send_follow_up_email(email, request_id)

if __name__ == "__main__":
    check_for_pending_requests()

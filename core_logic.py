import os
from dotenv import load_dotenv
import google.generativeai as genai

from email_utils import send_email_alert
from customer_ack import send_customer_acknowledgment
from db_utils import log_request

# Load environment variables and configure Gemini
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

# Contact directory
department_contacts = {
    "Logistics": {"name": "James Odhiambo", "email": "odanga.oketch@gmail.com"},
    "Billing": {"name": "Sarah Wambui", "email": "odanga.oketch@students.jkuat.ac.ke"},
    "HR": {"name": "Faith Chebet", "email": "hr@company.com"},
    "IT Support": {"name": "Kevin Otieno", "email": "itsupport@company.com"},
    "Customer Service": {"name": "Nancy Muthoni", "email": "support@company.com"},
    "Management": {"name": "Daniel Mwangi", "email": "management@company.com"},
}

def classify_department(user_message, user_email):
    prompt = f"""
You are a smart customer service assistant. Your job is to analyze a customer's complaint or request and assign it to the most relevant department.

Departments:
1. Logistics – order tracking, delivery issues, returns
2. Billing – payments, overcharges, refunds
3. HR – job applications, employee records
4. IT Support – system errors, tech issues
5. Customer Service – general inquiries, feedback
6. Management – escalations, audits, policy

Customer message: "{user_message}"
"""
    response = model.generate_content(prompt)
    answer_clean = response.text.strip().lower()

    departments = {
        "logistics": "Logistics",
        "billing": "Billing",
        "hr": "HR",
        "it support": "IT Support",
        "customer service": "Customer Service",
        "management": "Management"
    }

    for key in departments:
        if key in answer_clean:
            return departments[key]

    return "Customer Service"

def simulate_alert(department, user_message, user_email):
    contact = department_contacts.get(department)
    if contact:
        name = contact["name"]
        email = contact["email"]
        print(f"[ALERT] Routed to {department}: {name} ({email})")
        print(f"Message: {user_message}")
        print(f"Customer Email: {user_email}")
        send_email_alert(email, department, user_message, user_email)
        send_customer_acknowledgment(user_email, department)
    else:
        print(f"[ALERT] Department '{department}' not recognized.")

def handle_user_request(user_message, user_email):
    department = classify_department(user_message, user_email)
    simulate_alert(department, user_message, user_email)
    log_request(user_message, user_email, department)
    return (
        f"✅ Your request has been forwarded to the **{department}** department.\n\n"
        f"📨 A confirmation email has been sent to **{user_email}**. Our team will get back to you shortly."
    )

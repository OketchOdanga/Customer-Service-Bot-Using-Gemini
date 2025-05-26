import google.generativeai as genai
import gradio as gr
import os
from dotenv import load_dotenv
from email_utils import send_email_alert
from customer_ack import send_customer_acknowledgment
# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key securely
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")


# Simulated internal contact directory
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

Here is how the organization operates:

Organizational Units (Departments):

1. **Logistics** – Responsible for order tracking, delivery issues, and returns. (Internal team)
2. **Billing** – Handles payments, overcharges, refunds, and receipts. (Internal team)
3. **HR** – Manages job applications, employee records, and internal conflicts. (Internal use only)
4. **IT Support** – Solves system errors, website problems, and offers technical support. (Internal & Customer-facing)
5. **Customer Service** – Responds to general inquiries, collects feedback, and triages customer issues. (Public-facing)
6. **Management** – Deals with escalated issues, audits, and policy matters. (Internal – for escalations only)

Based on the customer's message below, assign it to the most relevant department.
ONLY return the name of the department.

Customer message: "{user_message}"
"""

    response = model.generate_content(prompt)
    answer = response.text.strip()

    # Normalize the response for matching
    answer_clean = answer.lower()

    departments = {
        "logistics": "Logistics",
        "billing": "Billing",
        "hr": "HR",
        "it support": "IT Support",
        "customer service": "Customer Service",
        "management": "Management"
    }

    # Match response to known departments
    for key in departments:
        if key in answer_clean:
            return departments[key]

    # Fallback if unclear or unmatched
    return "Customer Service"

""" #Alert Simulation Function
def simulate_alert(department, message):
    contact = department_contacts.get(department, {"name": "Unknown", "email": "unknown@company.com"})
    print("\n" + "=" * 50)
    print(f"[ALERT] Request routed to {department} Department.")
    print(f"Assigned to: {contact['name']} ({contact['email']})")
    print(f"Message: {message}")
    print("=" * 50 + "\n") """

def simulate_alert(department, user_message, user_email):
    contact = department_contacts.get(department)
    if contact:
        name = contact["name"]
        email = contact["email"]
        print(f"[ALERT] Routed to {department}: {name} ({email})")
        print(f"Message: {user_message}")
        print(f"Customer Email: {user_email}")
        
        # Send email to department
        send_email_alert(email, department, user_message, user_email)
        # Send acknowledgment to customer
        send_customer_acknowledgment(user_email, department)
    else:
        print(f"[ALERT] Department '{department}' not recognized.")


#Trigger the Alert After Classification
def handle_user_request(user_message, user_email):
    department = classify_department(user_message, user_email)
    simulate_alert(department, user_message, user_email)
    return (
    f"✅ Your request has been forwarded to the **{department}** department.\n\n"
    f"📨 A confirmation email has been sent to **{user_email}**. Our team will get back to you shortly."
)



# Gradio interface
iface = gr.Interface(
    fn=handle_user_request,
    inputs=[
        gr.Textbox(label="Enter your complaint or request"),
        gr.Textbox(label="Enter your email address")
    ],
    outputs=gr.Markdown(label="Routing Result"),
    title="AI Customer Service Agent"
)


if __name__ == "__main__":
    iface.launch(share=True)


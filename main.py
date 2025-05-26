import google.generativeai as genai
import gradio as gr
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key securely
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

def classify_department(message):
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

Customer message: "{message}"
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

demo = gr.Interface(fn=classify_department, 
                    inputs="text", 
                    outputs="text",
                    title="Customer Service Bot",
                    description="Enter a customer complaint to get the relevant department.")

demo.launch(share=True)


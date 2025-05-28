from flask import request
from flask import Flask, jsonify
import sqlite3
from scheduler import start_scheduler
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Load environment variables
load_dotenv()

API_SECRET_KEY = os.getenv("API_SECRET_KEY")

app = Flask(__name__)
CORS(app)

DB_NAME = "requests.db"

def get_requests_from_db(status_filter=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if status_filter:
        cursor.execute("SELECT * FROM requests WHERE status = ?", (status_filter,))
    else:
        cursor.execute("SELECT * FROM requests")

    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "message": row[1],
            "email": row[2],
            "department": row[3],
            "timestamp": row[4],
            "status": row[5]
        })

    return result

@app.route("/")
def index():
    return "API is running. Use /requests or /requests/<status>"


@app.route("/requests", methods=["GET"])
def get_all_requests():
    data = get_requests_from_db()
    return jsonify(data), 200

@app.route("/requests/<status>", methods=["GET"])
def get_requests_by_status(status):
    data = get_requests_from_db(status_filter=status.capitalize())
    return jsonify(data), 200

@app.route("/requests/<int:req_id>/response", methods=["POST"])
def update_response(req_id):
    data = request.json
    new_response = data.get("response")
    new_status = data.get("status", "Pending")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE requests
        SET response = ?, status = ?
        WHERE id = ?
    ''', (new_response, new_status, req_id))

    conn.commit()
    conn.close()

    return jsonify({"message": "Response and status updated successfully."}), 200

@app.route("/api/submit", methods=["POST"])
def submit_request():
    api_key = request.headers.get("x-api-key")

    if api_key != API_SECRET_KEY:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    message = data.get("message")
    email = data.get("email")
    department = data.get("department")

    # Validate fields
    if not all([message, email, department]):
        return jsonify({"error": "Missing fields"}), 400

    # Log to DB, send email, etc.
    # log_request(...) ← your existing logging function

    return jsonify({"message": "Request submitted successfully."}), 201

if __name__ == "__main__":
    start_scheduler()
    app.run(debug=True)

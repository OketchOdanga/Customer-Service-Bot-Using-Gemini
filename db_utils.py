import sqlite3
from datetime import datetime

DB_NAME = "requests.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    conn.commit()
    conn.close()

def log_request(message, email, department):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requests (message, email, department, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (message, email, department, timestamp))
    conn.commit()
    conn.close()

# migrate_add_response_column.py
import sqlite3

DB_NAME = "requests.db"

def add_response_column():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Check if 'response' column already exists
    cursor.execute("PRAGMA table_info(requests)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if "response" not in columns:
        cursor.execute("ALTER TABLE requests ADD COLUMN response TEXT DEFAULT ''")
        conn.commit()
        print("[DB MIGRATION] 'response' column added.")
    else:
        print("[DB MIGRATION] 'response' column already exists.")

    conn.close()

if __name__ == "__main__":
    add_response_column()

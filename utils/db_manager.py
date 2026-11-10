import sqlite3
from datetime import datetime

DB_PATH = "data/qa_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qa_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_qa(question: str, answer: str, user_id: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO qa_history (user_id, question, answer, timestamp)
        VALUES (?, ?, ?, ?)
    """, (user_id, question, answer, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

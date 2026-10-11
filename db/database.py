import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../cloudcell_support.db")

def init_db():
    """SQLite veritabanını ve destek biletleri tablosunu oluşturur."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT NOT NULL,
            service_type TEXT NOT NULL,
            issue_description TEXT NOT NULL,
            priority TEXT NOT NULL,
            ai_diagnosis TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_ticket(customer_id: str, service_type: str, issue_description: str, priority: str, ai_diagnosis: str, status: str):
    """Analiz edilen destek biletini veritabanına kaydeder."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO support_tickets (customer_id, service_type, issue_description, priority, ai_diagnosis, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (customer_id, service_type, issue_description, priority, ai_diagnosis, status))
    conn.commit()
    conn.close()

def fetch_all_tickets():
    """Veritabanındaki tüm biletleri getirir."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, customer_id, service_type, priority, status, created_at FROM support_tickets")
    rows = cursor.fetchall()
    conn.close()
    return rows
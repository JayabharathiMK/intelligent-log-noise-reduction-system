import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "log_noise_system.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Create Users Login Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            login_time TIMESTAMP
        )
    ''')
    
    # Create Processed Logs Table (optional, for history)
    c.execute('''
        CREATE TABLE IF NOT EXISTS processed_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_name TEXT,
            created_at TIMESTAMP,
            content BLOB
        )
    ''')
    
    conn.commit()
    conn.close()

def log_user_login(email):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO user_logins (email, login_time) VALUES (?, ?)", (email, datetime.now()))
    conn.commit()
    conn.close()

def get_all_user_logins():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM user_logins ORDER BY login_time DESC", conn)
    conn.close()
    return df

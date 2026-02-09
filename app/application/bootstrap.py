# app/application/bootstrap.py

import sqlite3
import os
from app.application.config import settings

def init_api_key_db():
    if not os.path.exists(settings.DB_DIR):
        os.makedirs(settings.DB_DIR)

    if settings.DB_TYPE == "sqlite":
        conn = sqlite3.connect(settings.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_hash TEXT UNIQUE NOT NULL,
                owner TEXT NOT NULL,
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    elif settings.DB_TYPE == "postgresql":
        pass

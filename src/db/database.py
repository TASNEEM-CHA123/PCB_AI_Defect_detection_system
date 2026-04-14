import sqlite3
import os
import datetime

class Database:
    def __init__(self, db_path="src/db/industrial_pcb.db"):
        self.db_path = db_path
        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inspections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operator_id TEXT,
                    timestamp TEXT,
                    serial_number TEXT,
                    defect_count INTEGER,
                    severity TEXT,
                    status TEXT
                )
            ''')
            conn.commit()

    def log_inspection(self, operator_id, serial_number, defect_count, severity, status):
        timestamp = datetime.datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO inspections (operator_id, timestamp, serial_number, defect_count, severity, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (operator_id, timestamp, serial_number, defect_count, severity, status))
            conn.commit()
            return cursor.lastrowid

    def get_history(self, limit=50):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, operator_id, timestamp, serial_number, defect_count, severity, status 
                FROM inspections 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

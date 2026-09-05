# durable local events queue for Git events, with SQLite backend
import sqlite3
from pathlib import Path
from typing import Optional

class EventStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        
    def initialize(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    event_data TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """

import sqlite3
from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "installation_history.db"


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS installation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_id TEXT NOT NULL,
                tool_name TEXT NOT NULL,
                status TEXT NOT NULL,
                message TEXT,
                timestamp TEXT NOT NULL
            )
        """)

        connection.commit()


def record_installation(tool_id, tool_name, status, message):
    initialize_database()

    timestamp = datetime.now().astimezone().isoformat(
        timespec="seconds"
    )

    with get_connection() as connection:
        connection.execute("""
            INSERT INTO installation_history
            (tool_id, tool_name, status, message, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            tool_id,
            tool_name,
            status,
            message,
            timestamp
        ))

        connection.commit()


def get_installation_history(limit=100):
    initialize_database()

    with get_connection() as connection:
        rows = connection.execute("""
            SELECT id, tool_id, tool_name, status, message, timestamp
            FROM installation_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

    return [dict(row) for row in rows]

import sqlite3
from pathlib import Path


DATABASE_PATH = Path("data/rail_data.db")


def create_database():
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id TEXT NOT NULL,
            station_name TEXT NOT NULL,
            line TEXT,
            destination TEXT NOT NULL,
            scheduled_time TEXT NOT NULL,
            expected_time TEXT,
            collected_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


create_database()

print("Database created successfully.")
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

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS unique_departure
        ON departures (
            station_id,
            line,
            destination,
            scheduled_time
        )
    """)

    connection.commit()
    connection.close()


def save_departure(
    station_id,
    station_name,
    line,
    destination,
    scheduled_time,
    expected_time
):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO departures (
            station_id,
            station_name,
            line,
            destination,
            scheduled_time,
            expected_time,
            collected_at
        )
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
        ON CONFLICT (
            station_id,
            line,
            destination,
            scheduled_time
        )
        DO UPDATE SET
            expected_time = excluded.expected_time,
            collected_at = datetime('now')
        """,
        (
            station_id,
            station_name,
            line,
            destination,
            scheduled_time,
            expected_time
        )
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully.")
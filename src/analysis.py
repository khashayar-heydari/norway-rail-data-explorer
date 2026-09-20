import sqlite3

from database import DATABASE_PATH


def get_departure_count():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM departures")

    count = cursor.fetchone()[0]

    connection.close()

    return count


departure_count = get_departure_count()

print(f"Departures stored in database: {departure_count}")
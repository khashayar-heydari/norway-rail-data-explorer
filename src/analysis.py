import sqlite3
from datetime import datetime

from database import DATABASE_PATH


def get_departures():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            line,
            destination,
            scheduled_time,
            expected_time
        FROM departures
        ORDER BY scheduled_time
    """)

    departures = cursor.fetchall()

    connection.close()

    return departures


def calculate_delay(scheduled_time, expected_time):
    if not expected_time:
        return None

    scheduled = datetime.fromisoformat(scheduled_time)
    expected = datetime.fromisoformat(expected_time)

    difference = expected - scheduled

    return difference.total_seconds() / 60


def main():
    departures = get_departures()

    print(f"Departures stored in database: {len(departures)}")

    for line, destination, scheduled_time, expected_time in departures:
        delay = calculate_delay(
            scheduled_time,
            expected_time
        )

        scheduled_display = datetime.fromisoformat(
            scheduled_time
        ).strftime("%H:%M")

        if expected_time:
            expected_display = datetime.fromisoformat(
                expected_time
            ).strftime("%H:%M")
        else:
            expected_display = "-"

        print()
        print(f"{line} -> {destination}")
        print(f"Scheduled: {scheduled_display}")
        print(f"Expected:  {expected_display}")

        if delay is None:
            print("Delay:     Unknown")
        else:
            print(f"Delay:     {delay:.1f} minutes")


if __name__ == "__main__":
    main()
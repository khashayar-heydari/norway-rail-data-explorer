import sqlite3
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

from database import DATABASE_PATH


OUTPUT_PATH = Path("output/average_delay_by_station.png")


def calculate_delay(scheduled_time, expected_time):
    if not expected_time:
        return None

    scheduled = datetime.fromisoformat(scheduled_time)
    expected = datetime.fromisoformat(expected_time)

    difference = expected - scheduled

    return difference.total_seconds() / 60


def get_departures():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            station_name,
            scheduled_time,
            expected_time
        FROM departures
    """)

    departures = cursor.fetchall()

    connection.close()

    return departures


def main():
    departures = get_departures()

    station_delays = {}

    for station_name, scheduled_time, expected_time in departures:
        delay = calculate_delay(
            scheduled_time,
            expected_time
        )

        if delay is None or delay <= 0:
            continue

        if station_name not in station_delays:
            station_delays[station_name] = []

        station_delays[station_name].append(delay)

    station_names = []
    average_delays = []

    for station_name, delays in station_delays.items():
        average_delay = sum(delays) / len(delays)

        station_names.append(station_name)
        average_delays.append(average_delay)

    if not station_names:
        print("No delayed departures found.")
        return

    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    plt.figure(figsize=(9, 5))
    plt.bar(station_names, average_delays)

    plt.title("Average Delay Among Delayed Departures by Station")
    plt.xlabel("Station")
    plt.ylabel("Average delay (minutes)")

    plt.xticks(rotation=20)
    plt.tight_layout()

    plt.savefig(OUTPUT_PATH)

    print(f"Chart saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
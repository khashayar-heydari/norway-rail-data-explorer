import sqlite3
from datetime import datetime

from database import DATABASE_PATH


def get_departures():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            station_name,
            line,
            destination,
            scheduled_time,
            expected_time
        FROM departures
        ORDER BY station_name, scheduled_time
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

    delays = []

    for station_name, line, destination, scheduled_time, expected_time in departures:
        delay = calculate_delay(scheduled_time, expected_time)

        if delay is not None:
            delays.append(delay)

    delayed_departures = [
        delay for delay in delays if delay > 0
    ]

    on_time_departures = [
        delay for delay in delays if delay <= 0
    ]

    print("Overall summary")
    print("---------------")
    print(f"Total departures: {len(departures)}")
    print(f"Delayed departures: {len(delayed_departures)}")
    print(f"On-time departures: {len(on_time_departures)}")

    if delayed_departures:
        average_delay = sum(delayed_departures) / len(delayed_departures)
        largest_delay = max(delayed_departures)

        print(f"Average delay: {average_delay:.1f} minutes")
        print(f"Largest delay: {largest_delay:.1f} minutes")

    station_data = {}

    for station_name, line, destination, scheduled_time, expected_time in departures:
        if station_name not in station_data:
            station_data[station_name] = []

        delay = calculate_delay(scheduled_time, expected_time)

        station_data[station_name].append(delay)

    print()
    print("Station summary")
    print("---------------")

    for station_name, station_delays in station_data.items():
        known_delays = [
            delay for delay in station_delays if delay is not None
        ]

        delayed = [
            delay for delay in known_delays if delay > 0
        ]

        print()
        print(station_name)
        print(f"Departures: {len(station_delays)}")
        print(f"Delayed: {len(delayed)}")

        if delayed:
            average_delay = sum(delayed) / len(delayed)
            print(f"Average delay: {average_delay:.1f} minutes")
        else:
            print("Average delay: 0.0 minutes")

    print()
    print("Departure details")
    print("-----------------")

    for station_name, line, destination, scheduled_time, expected_time in departures:
        delay = calculate_delay(scheduled_time, expected_time)

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
        print(f"{station_name}")
        print(f"{line} -> {destination}")
        print(f"Scheduled: {scheduled_display}")
        print(f"Expected:  {expected_display}")

        if delay is None:
            print("Delay:     Unknown")
        else:
            print(f"Delay:     {delay:.1f} minutes")


if __name__ == "__main__":
    main()
import requests

from database import create_database, save_departure


GEOCODER_URL = "https://api.entur.io/geocoder/v3/autocomplete"
JOURNEY_PLANNER_URL = "https://api.entur.io/journey-planner/v3/graphql"

HEADERS = {
    "ET-Client-Name": "khashayar-norway-rail-data-explorer"
}


def search_station(station_name):
    params = {
        "q": station_name,
        "lang": "no",
        "limit": 1,
        "layers": "stopPlace",
        "stopPlaceTypes": "railStation"
    }

    response = requests.get(
        GEOCODER_URL,
        headers=HEADERS,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if not data["features"]:
        return None

    station = data["features"][0]

    return {
        "name": station["properties"]["names"]["display"],
        "id": station["properties"]["id"]
    }


def get_departures(stop_place_id):
    query = """
    {
      stopPlace(id: "%s") {
        estimatedCalls(numberOfDepartures: 5) {
          aimedDepartureTime
          expectedDepartureTime

          destinationDisplay {
            frontText
          }

          serviceJourney {
            line {
              publicCode
            }
          }
        }
      }
    }
    """ % stop_place_id

    response = requests.post(
        JOURNEY_PLANNER_URL,
        headers=HEADERS,
        json={"query": query},
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def main():
    create_database()

    station_name = input("Enter station: ")
    station = search_station(station_name)

    if not station:
        print("Station not found")
        return

    print()
    print("Station:", station["name"])
    print("ID:", station["id"])

    departures = get_departures(station["id"])

    calls = departures["data"]["stopPlace"]["estimatedCalls"]

    for call in calls:
        line = call["serviceJourney"]["line"]["publicCode"]
        destination = call["destinationDisplay"]["frontText"]

        scheduled_time = call["aimedDepartureTime"]
        expected_time = call["expectedDepartureTime"]

        scheduled_display = scheduled_time[11:16]

        if expected_time:
            expected_display = expected_time[11:16]
        else:
            expected_display = "-"

        print()
        print(f"{line} -> {destination}")
        print(f"Scheduled: {scheduled_display}")
        print(f"Expected:  {expected_display}")

        save_departure(
            station["id"],
            station["name"],
            line,
            destination,
            scheduled_time,
            expected_time
        )


if __name__ == "__main__":
    main()
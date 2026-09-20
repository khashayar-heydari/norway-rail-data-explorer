import requests

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


station = search_station("Tønsberg")

if station:
    print("Station:", station["name"])
    print("ID:", station["id"])

    departures = get_departures(station["id"])

    calls = departures["data"]["stopPlace"]["estimatedCalls"]

    for call in calls:
        line = call["serviceJourney"]["line"]["publicCode"]
        destination = call["destinationDisplay"]["frontText"]

        scheduled = call["aimedDepartureTime"][11:16]
        expected = call["expectedDepartureTime"][11:16]

        print()
        print(f"{line} -> {destination}")
        print(f"Scheduled: {scheduled}")
        print(f"Expected:  {expected}")

else:
    print("Station not found")
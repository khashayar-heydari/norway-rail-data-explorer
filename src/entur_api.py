import requests


BASE_URL = "https://api.entur.io/geocoder/v3/autocomplete"

HEADERS = {
    "ET-Client-Name": "khashayar-norway-rail-data-explorer"
}


def search_station(station_name):
    params = {
        "q": station_name,
        "lang": "no",
        "limit": 5,
        "layers": "stopPlace",
        "stopPlaceTypes": "railStation",
    }

    response = requests.get(
        BASE_URL,
        headers=HEADERS,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


data = search_station("Tønsberg")

for feature in data["features"]:
    properties = feature["properties"]

    print("Name:", properties["names"]["display"])
    print("ID:", properties["id"])
    print("Coordinates:", feature["geometry"]["coordinates"])
    print()
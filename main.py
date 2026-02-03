from fastapi import FastAPI, Query
import requests

app = FastAPI()

BASE_URL = "https://api.openaq.org/v3"
API_KEY = "ed7c82477911ee7eba20b6ac4f8647878331e877c3efdbff59db123027b84d61"

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

@app.get("/airquality")
def get_air_quality(city: str = Query(..., description="City name")):
    # 1️⃣ Get locations for the city
    locations_url = f"{BASE_URL}/locations"
    params = {
        "city": city,
        "limit": 5
    }

    locations_response = requests.get(
        locations_url,
        headers=HEADERS,
        params=params
    )

    locations_data = locations_response.json()

    if not locations_data.get("results"):
        return {"error": f"No locations found for {city}"}

    output = []

    # 2️⃣ Loop through locations
    for location in locations_data["results"]:
        location_id = location["id"]
        location_name = location["name"]

        sensors = location.get("sensors", [])

        # 3️⃣ Loop through sensors
        for sensor in sensors:
            sensor_id = sensor["id"]
            parameter = sensor["parameter"]["name"]

            # 4️⃣ Get latest measurement
            measurements_url = f"{BASE_URL}/sensors/{sensor_id}/measurements"
            measurements_response = requests.get(
                measurements_url,
                headers=HEADERS,
                params={"limit": 1}
            )

            measurements_data = measurements_response.json()

            if not measurements_data.get("results"):
                continue

            measurement = measurements_data["results"][0]

            output.append({
                "city": city,
                "location_id": location_id,
                "location_name": location_name,
                "sensor_id": sensor_id,
                "pollutant": parameter,
                "value": measurement["value"],
                "unit": measurement["parameter"]["units"],
                "time": measurement["period"]["datetimeFrom"]["utc"]
            })

    return output

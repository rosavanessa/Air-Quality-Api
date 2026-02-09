from fastapi import FastAPI, Query
import requests

from database import (
    get_or_create_city,
    get_or_create_location,
    get_or_create_sensor,
    insert_measurement
)

app = FastAPI()

BASE_URL = "https://api.openaq.org/v3"
API_KEY = "ed7c82477911ee7eba20b6ac4f8647878331e877c3efdbff59db123027b84d61"

HEADERS = {
    "X-API-Key": API_KEY
}

@app.get("/airquality")
def fetch_air_quality(city: str = Query(...)):

    resp = requests.get(
        f"{BASE_URL}/locations",
        headers=HEADERS,
        params={"city": city, "limit": 5},
        timeout=10
    ).json()

    if not resp.get("results"):
        return {"error": "City not found"}

    country_field = resp["results"][0].get("country")

    if isinstance(country_field, dict):
        country_code = country_field.get("code")
    else:
        country_code = country_field

    city_id = get_or_create_city(city, country_code)

    for loc in resp["results"][:2]:
        location_id = loc["id"]
        location_name = loc["name"]

        get_or_create_location(location_id, location_name, city_id)

        for sensor in loc.get("sensors", [])[:2]:
            sensor_id = sensor["id"]
            parameter = sensor["parameter"]["name"]

            get_or_create_sensor(sensor_id, parameter, location_id)

            meas_resp = requests.get(
                f"{BASE_URL}/sensors/{sensor_id}/measurements",
                headers=HEADERS,
                params={"limit": 1},
                timeout=10
            ).json()

            if not meas_resp.get("results"):
                continue

            m = meas_resp["results"][0]

            insert_measurement(
                sensor_id=sensor_id,
                value=m["value"],
                unit=m["parameter"]["units"],
                measured_at=m["period"]["datetimeFrom"]["utc"]
            )

    return {"status": "Data fetched and saved"}


@app.get("/airquality")
def get_air_quality(city: str):

    get_latest_measurements_for_city = ["results"][0].get("city")
    """
    Returns latest measurements for a city
    """
    return get_latest_measurements_for_city(city)


@app.post("/ingest/airquality")
def ingest_air_quality(city: str = Query(...)):
    ...



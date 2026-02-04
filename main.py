from fastapi import FastAPI, Query
import requests
from database import get_db

app = FastAPI()

BASE_URL = "https://api.openaq.org/v3"
API_KEY = "YOUR_API_KEY"

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

@app.get("/airquality")
def fetch_air_quality(city: str = Query(...)):

    db = get_db()
    cursor = db.cursor()

    # =========================
    # 1️⃣ FETCH LOCATIONS
    # =========================
    locations_resp = requests.get(
        f"{BASE_URL}/locations",
        headers=HEADERS,
        params={"city": city, "limit": 5}
    ).json()

    if not locations_resp.get("results"):
        return {"error": "City not found"}

    country_code = locations_resp["results"][0]["country"]

    # =========================
    # 2️⃣ COUNTRY
    # =========================
    cursor.execute(
        "SELECT country_code FROM countries WHERE country_code=%s",
        (country_code,)
    )

    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO countries (country_code) VALUES (%s)",
            (country_code,)
        )
        db.commit()

    # =========================
    # 3️⃣ CITY
    # =========================
    cursor.execute(
        "SELECT city_id FROM cities WHERE city_name=%s",
        (city,)
    )
    row = cursor.fetchone()

    if row:
        city_id = row[0]
    else:
        cursor.execute(
            "INSERT INTO cities (city_name, country_code) VALUES (%s, %s)",
            (city, country_code)
        )
        db.commit()
        city_id = cursor.lastrowid

    # =========================
    # 4️⃣ LOCATIONS
    # =========================
    for loc in locations_resp["results"]:
        location_id = loc["id"]
        location_name = loc["name"]

        cursor.execute(
            "SELECT location_id FROM locations WHERE location_id=%s",
            (location_id,)
        )

        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO locations (location_id, location_name, city_id) VALUES (%s, %s, %s)",
                (location_id, location_name, city_id)
            )
            db.commit()

        # =========================
        # 5️⃣ SENSORS
        # =========================
        for sensor in loc.get("sensors", []):
            sensor_id = sensor["id"]
            parameter = sensor["parameter"]["name"]

            cursor.execute(
                "SELECT sensor_id FROM sensors WHERE sensor_id=%s",
                (sensor_id,)
            )

            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO sensors (sensor_id, parameter, location_id) VALUES (%s, %s, %s)",
                    (sensor_id, parameter, location_id)
                )
                db.commit()

            # =========================
            # 6️⃣ MEASUREMENTS
            # =========================
            meas = requests.get(
                f"{BASE_URL}/sensors/{sensor_id}/measurements",
                headers=HEADERS,
                params={"limit": 1}
            ).json()

            if not meas.get("results"):
                continue

            m = meas["results"][0]

            cursor.execute(
                """
                INSERT INTO measurements (sensor_id, value, unit, measured_at)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    sensor_id,
                    m["value"],
                    m["parameter"]["units"],
                    m["period"]["datetimeFrom"]["utc"]
                )
            )
            db.commit()

    return {"status": "Data fetched and saved"}

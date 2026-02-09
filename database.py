import mysql.connector

def get_db():
    db = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = "",
        database = "air quality"

)

    print("Database connection successful")
    return db

def get_or_create_country(country_code):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT Country_Code FROM countries WHERE Country_Code = %s",
        (country_code,)
    )
    row = cursor.fetchone()

    if row:
        return country_code

    cursor.execute(
        "INSERT INTO countries (Country_Code) VALUES (%s)",
        (country_code,)
    )
    db.commit()

    return country_code


def get_or_create_city(city_name, country_code):
    db = get_db()
    cursor = db.cursor()

    get_or_create_country(country_code)


    cursor.execute(
        "SELECT city_id FROM cities WHERE city_name = %s",
        (city_name,)
    )
    row = cursor.fetchone()

    if row:
        return row[0]

    cursor.execute(
        "INSERT INTO cities (city_name, country_code) VALUES (%s, %s)",
        (city_name, country_code)
    )
    db.commit()

    return cursor.lastrowid

def get_or_create_location(location_id, location_name, city_id):
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute(
        "SELECT location_id FROM locations WHERE location_id = %s",
        (location_id,)

    )
    
        row = cursor.fetchone()

        if row: 
             return row[0]
        else:
            cursor.execute(
                "INSERT into locations(location_id, location_name, city_id) VALUES (%s, %s, %s)",
                (location_id, location_name, city_id)
        )
        db.commit()

        return location_id

def get_or_create_sensor(sensor_id, parameter, location_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT sensor_id FROM sensors WHERE sensor_id = %s",
        (sensor_id,)
    )
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        cursor.execute(
            "INSERT INTO sensors (sensor_id, parameter, location_id) VALUES (%s, %s, %s)",
            (sensor_id, parameter, location_id)
        )
        db.commit()
        return sensor_id

def insert_measurement(sensor_id, value, unit, measured_at):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO measurements (sensor_id, value, unit, measured_at) VALUES (%s, %s, %s, %s)",
        (sensor_id, value, unit, measured_at)
    )
    db.commit()

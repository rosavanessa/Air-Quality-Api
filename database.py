import mysql.connector

def get_db():
    return mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = "",
    database = "air quality"

)

print("Database connection successful")

def get_or_create_city(city_name, country_code):
    db = get_db()
    cursor = db.cursor()

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
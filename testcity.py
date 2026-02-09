from database import get_or_create_city
from database import get_or_create_location
from database import get_or_create_sensor

city_id = get_or_create_city("Capetown", "SA")
location_id = get_or_create_location(10,"NIMS", 4)
sensor_id = get_or_create_sensor(8, "PM10", 10 )
print ("location_ID",location_id)
print("City_ID: ", city_id)
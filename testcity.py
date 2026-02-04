from database import get_or_create_city

city_id = get_or_create_city("Nairobi", "KE")
print("City_ID: ", city_id)
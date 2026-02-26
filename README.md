Global Air Quality Analytics Dashboard
Project Overview
This project is a backend air quality monitoring system built using FastAPI that integrates with the OpenAQ v3 API to fetch real-time environmental data and store it in a structured database.
The system allows users to query air quality data by city and dynamically retrieve live environmental measurements from OpenAQ.

What this Project does:
Connects to the OpenAQ v3 API

Authenticates using a secure API key

Fetches real-time air quality data by city

Processes and structures environmental sensor data

Designed to store data into a relational database

Built using modern backend architecture principles


Tech Stack
Python 
FastAPI
Requests 
Uvicorn
OpenAQ v3 API
Relational Database


How It Works:

User sends a GET request:

/airquality?city=Nairobi

The API:

Calls OpenAQ v3 /locations endpoint

Passes the city as a query parameter

Authenticates using X-API-Key

Retrieves structured location + sensor data

Returns clean JSON response

Stores structured measurements in database


Future Improvements

Store time-series measurements

Add historical data analytics

Build frontend dashboard (React / Angular)

Add air quality index (AQI) classification

Deploy to cloud (Render / Railway / AWS)

Add scheduled background jobs for automatic updates

Implement authentication for users

Build environmental risk prediction model


Project Structure
air-quality/
│
├── main.py
├── database.py
├── requirements.txt
└── README.md


Setup Instructions:

1.Clone repository

2.Install dependencies

pip install -r requirements.txt

3.Add your OpenAQ API key

4.Run server:

uvicorn main:app --reload

5.Visit:

http://127.0.0.1:8000/airquality?city=Nairobi

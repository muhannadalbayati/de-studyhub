# Purpose: Extract weather data from an API and load it into PostgreSQL.
# Inputs: Open-Meteo API responses and PostgreSQL database connection.
# Outputs: weather_readings table populated with 8 records and verification query results.


# Import Libraries ------------------------------------------
import requests
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


# Function ------------------------------------------------- 
def get_connection():
    """
        Creates and returns a connection to the de_practice database.
        Credentials are loaded from .env — never hardcoded.
        Returns: psycopg2 connection object
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

# Function ------------------------------------------------- 
def fetch_weather(city, latitude, longitude):
    """
    Fetches current weather data from Open-Meteo API.    
    Parameters:
        city (string) --> The city 
        latitude (float) --> Location latitude
        longitude (float) --> Location longitude    
    Returns:
        dict (dictionary) --> Current weather data including temperature_2m,wind_speed_10m,relative_humidity_2m
    """
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m,relative_humidity_2m"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    weather = response.json()

    city_weather = weather["current"]
    city_dict = {
       "city": city,                 
       "temperature_c": city_weather['temperature_2m'],                 
       "wind_speed_kmh": city_weather['wind_speed_10m'],
       "humidity_pct": city_weather['relative_humidity_2m'],                 
      
    }
    return city_dict
    
# Function ------------------------------------------------- 
def create_table(cursor):
    """
    Creates the weather_readings table in PostgreSQL if it does not already exist.
    Parameters:
        cursor: PostgreSQL database cursor used to execute SQL statements.
    Returns:
        None
    """
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS weather_readings (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100) NOT NULL,
            temperature_c NUMERIC(5,2),
            wind_speed_kmh NUMERIC(5,2),
            humidity_pct INTEGER,
            fetched_at TIMESTAMP DEFAULT NOW()
        )"""
    )
    cursor.execute("TRUNCATE TABLE weather_readings RESTART IDENTITY;")

# Function ------------------------------------------------- 
def load_data(cursor, df):
    """
    Load weather data from a DataFrame into the database.
    Parameters:
        cursor: Database cursor object.
        df: DataFrame containing weather data.
    Returns:
        int: Number of rows inserted.
    """
    rows_inserted = 0

    for index, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO weather_readings (
                city,
                temperature_c,
                wind_speed_kmh,
                humidity_pct
            )
            VALUES (%s, %s, %s, %s)
            """,
            (row["city"], row["temperature_c"], row["wind_speed_kmh"], row["humidity_pct"])
        )

        rows_inserted += 1

    return rows_inserted

# Function ------------------------------------------------- 
def verify(cursor):
    """
    Run a verification query to confirm data has been loaded correctly
    and display cities ranked by temperature.
    Parameters:
        cursor: PostgreSQL database cursor used to execute SQL statements.
    Returns:
        list: Rows returned from the verification query.
    """

    cursor.execute("""
        SELECT city, temperature_c, humidity_pct
        FROM weather_readings
        ORDER BY temperature_c DESC;
    """)

    rows = cursor.fetchall()

    print("\n Verification Results (Cities ranked by temperature):")
    print("-" * 60)

    for row in rows:
        print(row)

    return rows





# Main -------------------------------------------------
cities = [
    {"city": "London",    "lat": 51.51, "lon": -0.13},
    {"city": "Paris",     "lat": 48.85, "lon": 2.35},
    {"city": "Berlin",    "lat": 52.52, "lon": 13.41},
    {"city": "Madrid",    "lat": 40.42, "lon": -3.70},
    {"city": "Amsterdam", "lat": 52.37, "lon": 4.90},
    {"city": "Dubai",     "lat": 25.20, "lon": 55.27},
    {"city": "New York",  "lat": 40.71, "lon": -74.01},
    {"city": "Tokyo",     "lat": 35.68, "lon": 139.69},
]

weather_data = []

for city in cities:                      
    weather = fetch_weather(city['city'], city['lat'], city['lon']) 
    weather_data.append(weather)

df = pd.DataFrame(weather_data)

conn = get_connection()
cursor = conn.cursor()

create_table(cursor)

row_count = load_data(cursor, df)

conn.commit()

verify(cursor)

print(f"\nRows inserted: {row_count}")

cursor.close()
conn.close()

# Purpose: Fetches current weather data for a list of cities using the Open-Meteo API.
# Input:   Hard-coded list of cities with lat/lon coordinates
# Output:  weather_results.csv — columns: city, temperature, windspeed

import requests
from pathlib import Path
import csv

script_dir = Path(__file__).resolve().parent
data_dir = script_dir.parent / "data"

def fetch_weather(latitude, longitude):
    """
    Fetches current weather data from Open-Meteo API.    
    Args:
        latitude (float): Location latitude
        longitude (float): Location longitude    
    Returns:
        dict: Current weather data including temperature and windspeed
    """
    url = "https://api.open-meteo.com/v1/forecast"
    
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    data = response.json()
    return data["current_weather"]

def write_csv(rows): 
    """
        Writes weather data for multiple cities to a CSV file.
        Args: rows (list): List of dicts with keys: city, temperature, windspeed
        Returns: None
    """  
    headers = ['city', 'temperature', 'windspeed']
    
    with open(data_dir/"weather_results.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:       
            writer.writerow(row)          
    return


cities = [
    {"name": "Baghdad", "lat": 33.3, "lon": 44.3},
    {"name": "Cairo",   "lat": 30.0, "lon": 31.2},
    {"name": "Paris",   "lat": 48.8, "lon": 2.3},
]

weather_data = []

for city in cities:                      
    weather = fetch_weather(city['lat'], city['lon'])    
    city_data = {
        "city": city['name'],
        "temperature": weather['temperature'],                 
        "windspeed": weather['windspeed']
    }
    weather_data.append(city_data)

write_csv(weather_data)

for c in weather_data:
    print("The City:", c['city'])
    print(f"Temperature: {c['temperature']}°C")
    print(f"Wind speed: {c['windspeed']} km/h")
    print("---------------------------------------")

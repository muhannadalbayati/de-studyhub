# Purpose: Fetches current weather data for a list of capital cities of countries using the Open-Meteo API.
# Input:   A list of countries, each with a capital city, latitude, and longitude — stored as a list of dicts
# Output:  data\country_weather.csv — columns: country, capital, temperature, windspeed, feels_like

import requests
from pathlib import Path
import csv

script_dir = Path(__file__).resolve().parent
data_dir = script_dir / "data"

def fetch_weather(latitude, longitude):
    """
    Fetches current weather data from Open-Meteo API.    
    Args:
        latitude (float) --> Location latitude
        longitude (float) --> Location longitude    
    Returns:
        dict (dictionary) --> Current weather data including temperature and windspeed
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
        Args: rows (list) --> List of dicts with keys: country, capital, temperature, windspeed, feels_like
        Returns: None
    """  
    headers = ['country', 'capital', 'temperature', 'windspeed', 'feels_like']
    
    with open(data_dir/"country_weather.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:       
            writer.writerow(row)          
    return

def feels_like(temperature):
    """
        Works out what a certain temperature feels like.
        Args: temperature (float) --> the temperature of a city
        Returns: feels_like_var (string) --> the associated feels like (Hot, Mild, Cold)
    """  
    if temperature >= 25:
        feels_like_var = "Hot"  
    elif temperature >= 15:
        feels_like_var = "Mild" 
    else:
        feels_like_var = "Cold"     
    return feels_like_var
    

def read_csv(data_file):
    """
        Read from CSV file, save in a dictionary variable (row),
        Args: data_file (string) --> the name of the CSV file to read
        Returns: rows (list) --> list of dicts, one per row in the CSV file
    """    
    with open(data_dir / data_file , newline='') as f:
        csvreader = csv.DictReader(f)
        rows = list(csvreader)    
    return rows

# ================ Main program ========================
capitals = [
    {"country": "Iraq", "capital": "Baghdad", "lat": 33.3, "lon": 44.3},
    {"country": "Egypt", "capital": "Cairo",   "lat": 30.0, "lon": 31.2},
    {"country": "France", "capital": "Paris",   "lat": 48.8, "lon": 2.3},
    {"country": "England", "capital": "London",   "lat": 51.5, "lon": -0.1},
]

weather_data = []

for capital in capitals:                      
    weather = fetch_weather(capital['lat'], capital['lon'])     

    city_data = {
        "country": capital['country'] ,
        "capital": capital['capital'],
        "temperature": weather['temperature'],                 
        "windspeed": weather['windspeed'],
        "feels_like": feels_like(weather['temperature'])
    }
    weather_data.append(city_data)

write_csv(weather_data)

data_file = "country_weather.csv"
weather_data = read_csv(data_file)
for c in weather_data:
    print("The country:", c['country'])
    print("The capital:", c['capital'])
    print(f"Temperature: {c['temperature']}°C")
    print(f"Wind speed: {c['windspeed']} km/h")
    print("Feels like:", c['feels_like'])
    print("---------------------------------------")

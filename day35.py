"""
Day 35 - Rain Alert App

tags: API keys, authentication, environment variables
"""
import os
from dotenv import load_dotenv
import requests

load_dotenv()

# Constants for OpenWeather API
API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
# Use environment variable to hide the API key from the code
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
print(API_KEY)
LATITUDE = -15.826691
LONGITUDE = -47.921822
API_PARAMETERS = {
    "lat": LATITUDE,
    "lon": LONGITUDE,
    "appid": API_KEY,
    "cnt": 4,
}

response = requests.get(
    API_ENDPOINT,
    params=API_PARAMETERS,
    timeout=10,
)
response.raise_for_status()
weather_data = response.json()
# print(weather_data["list"][0]["weather"][0]["id"])

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    # According to API documentation, codes below 700 are for rain
    if int(condition_code) < 700:
        will_rain = True
if will_rain:
    print("Bring an umbrella.")

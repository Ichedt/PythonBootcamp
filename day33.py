"""
Day 33 - ISS Tracker

tags: API
"""
import requests

# Pylint recomends using 'timeout' parameter to avoid waiting for a long time
# The timeout is in seconds
response = requests.get(url="http://api.open-notify.org/iss-now.json", timeout=10)

data = response.json()
longitude = data["iss_position"]["longitude"]
latitude = data["iss_position"]["latitude"]
iss_position = (longitude, latitude)

"""
Day 38 - Exercise Tracking with Sheets

tags: sheets, API, environment variables, POST requests
"""
import os
import datetime as dt
from dotenv import load_dotenv
import requests

load_dotenv()

# Nutritionix constants
GENDER = "male"
WEIGHT = 65
HEIGHT = 174
AGE = 22
NUTRITIONIX_EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
headers = {
    "x-app-id": os.getenv("NUTRITIONIX_APP_ID"),
    "x-app-key": os.getenv("NUTRITIONIX_API_KEY"),
}
# Sheety constants
SHEETY_GET = os.getenv("SHEETY_WORKOUTS_GET")
SHEETY_POST = os.getenv("SHEETY_WORKOUTS_POST")

# Nutritionix post exercise
exercise_text = input("Which exercises you did?: ")
exercise_params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,
}
response = requests.post(
    NUTRITIONIX_EXERCISE_ENDPOINT, json=exercise_params, headers=headers, timeout=10
)
result = response.json()

# Sheety post new row
today_date = dt.datetime.now().strftime("%d/%m/%Y")
now_time = dt.datetime.now().strftime("%X")
for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }
sheet_response = requests.post(SHEETY_GET, json=sheet_inputs, timeout=10)
print(sheet_response.text)

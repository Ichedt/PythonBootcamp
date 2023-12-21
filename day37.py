"""
Day 37 - Habit Tracker

tags: advanced authentication, post/put/delete requests
"""
import os
import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

# Date format yyyyMMdd
CONFIG_DATE = 20231220

PIXELA_TOKEN = os.getenv("PIXELA_TOKEN")
PIXELA_USERNAME = "ichedt"
PIXELA_GRAPH_ID = "graph1"
PIXELA_ENDPOINT = "https://pixe.la/v1/users"
PIXELA_GRAPH_ENDPOINT = f"{PIXELA_ENDPOINT}/{PIXELA_USERNAME}/graphs"
PIXELA_PIXEL_ENDPOINT = f"{PIXELA_ENDPOINT}/{PIXELA_USERNAME}/graphs/{PIXELA_GRAPH_ID}"
PIXELA_UPDATE_ENDPOINT = (
    f"{PIXELA_ENDPOINT}/{PIXELA_USERNAME}/graphs/{PIXELA_GRAPH_ID}/{CONFIG_DATE}"
)
PIXELA_DELETE_ENDPOINT = (
    f"{PIXELA_ENDPOINT}/{PIXELA_USERNAME}/graphs/{PIXELA_GRAPH_ID}/{CONFIG_DATE}"
)
headers = {"X-USER-TOKEN": PIXELA_TOKEN}

# Creating Pixela profile
# user_params = {
#     "token": PIXELA_TOKEN,
#     "username": PIXELA_USERNAME,
#     "agreeTermsOfService": "yes",
#     "notMinor": "yes",
# }
# response = requests.post(PIXELA_USERS_ENDPOINT, json=user_params, timeout=10)
#
# Access profile in: https://pixe.la/@ichedt

# Creating Pixela graph
# graph_params = {
#     "id": PIXELA_GRAPH_ID,
#     "name": "Cycling Graph",
#     "unit": "Km",
#     "type": "float",
#     "color": "shibafu",
# }
# response = requests.post(
#     PIXELA_GRAPH_ENDPOINT, json=graph_params, headers=headers, timeout=10
# )

# Adding a pixel
# The date format is yyyyMMdd
today = datetime.datetime.now()
pixel_params = {
    "date": today.strftime("%Y%m%d"),
    "quantity": "20.52",
}
response = requests.post(
    PIXELA_PIXEL_ENDPOINT, json=pixel_params, headers=headers, timeout=10
)

# Updating a pixel
# new_pixel_params = {
#     "quantity": "0",
# }
# response = requests.put(
#     PIXELA_UPDATE_ENDPOINT, json=new_pixel_params, headers=headers, timeout=10
# )

# Deleting a pixel
# requests.delete(PIXELA_DELETE_ENDPOINT, headers=headers, timeout=10)

print(response.text)

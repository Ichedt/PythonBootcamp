"""
Day 33 - ISS Tracker

tags: API
"""
import datetime as dt
import smtplib
import time
import requests

MY_LATITUDE = -15.826691
MY_LONGITUDE = -47.921822
MY_EMAIL = ""
MY_PASSWORD = ""


def is_iss_here():
    """Check the position of the ISS with the given latitude and logitude."""

    iss_response = requests.get("http://api.open-notify.org/iss-now.json", timeout=10)
    iss_response.raise_for_status()
    iss_data = iss_response.json()
    iss_latitude = float(iss_data["iss_position"]["latitude"])
    iss_longitude = float(iss_data["iss_position"]["longitude"])

    return (
        MY_LATITUDE - 5 <= iss_latitude <= MY_LATITUDE + 5
        and MY_LONGITUDE - 5 <= iss_longitude <= MY_LONGITUDE + 5
    )


def is_night():
    """Check if it is night on the given latitude and longitude."""

    # Parameters for the Sunrise-Sunset API
    parameters = {
        "lat": MY_LATITUDE,
        "lng": MY_LONGITUDE,
        "formatted": 0,
    }
    ss_response = requests.get(
        "https://api.sunrise-sunset.org/json", params=parameters, timeout=10
    )
    ss_response.raise_for_status()
    ss_data = ss_response.json()
    # Format the result using split() to get only the hours
    sunrise = int(ss_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(ss_data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = dt.datetime.now().hour

    return time_now >= sunset or time_now <= sunrise


while True:
    # Run the code every 60 seconds
    time.sleep(60)

    if is_iss_here() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject:Look Up\n\nThe ISS is above you in the sky!",
            )

"""
Day 39 - Cheap Flight Finder

tags: capstone project
"""
import datetime
import os
import sys
from dotenv import load_dotenv
import requests

load_dotenv()

SHEETY_FLIGHTDEALS_ENDPOINT = os.getenv("SHEETY_FLIGHTDEALS_ENDPOINT")
SHEETY_FLIGHTDEALS_TOKEN = os.getenv("SHEETY_FLIGHTDEALS_TOKEN")
SHEETY_FLIGHTDEALS_USERS_ENDPOINT = os.getenv("SHEETY_FLIGHTDEALS_USERS_ENDPOINT")
SHEETY_HEADERS = {
    "Authorization": f"Bearer {os.getenv("SHEETY_FLIGHTDEALS_TOEKN")}"
}
TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_HEADERS = {
    "apikey": os.getenv("TEQUILA_API_KEY")
}
ORIGIN_CITY_IATA = "LON"

class FlightData:
    """Class responsible for structuring the flight data."""

    def __init__(
        self,
        price: str,
        origin_city: str,
        origin_airport: str,
        destination_city: str,
        destination_airport: str,
        out_date: str,
        return_date: str,
        stop_overs: int=0,
        via_city: str=""
        ):
        """Construct all the flight data necessary for the search."""
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stop_overs = stop_overs
        self.via_city = via_city


class FlightSearch:
    """Class responsible for handling the Flight Search API."""

    def get_destination_code(self, city_name: str) -> str:
        """Get the IATA code for the given city."""
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(
            url=location_endpoint,
            headers=TEQUILA_HEADERS,
            params=query,
            timeout=10,
        )
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def check_flights(
        self,
        origin_city_code: str,
        destination_city_code: str,
        from_time: str,
        to_time: str,
    ) -> type[FlightData]:
        """Return a FlightData object with information about the flight."""
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 30,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "BRL",
        }
        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            headers=TEQUILA_HEADERS,
            params=query,
            timeout=10,
        )

        try:
            data = response.json()["data"][0]
        except IndexError:
            query["max_stopovers"] = 1
            response = requests.get(
                url=f"{TEQUILA_ENDPOINT}/v2/search",
                headers=TEQUILA_HEADERS,
                params=query,
                timeout=10,
            )
            data = response.json()["data"][0]
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][1]["cityTo"],
                destination_airport=data["route"][1]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][2]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][0]["cityTo"]
            )
            return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
            )
            return flight_data


class DataManager:
    """Class responsible for handling the data table."""

    def __init__(self):
        """Construct the attributes to manage the data.
        
        customer_data and city_codes attributes are defined None because they
        will be defined later on. So, to get rid of the "attribute defined
        outside __init__", they will be None at the beginning.
        """
        self.destination_data = {}
        self.customer_data = None
        self.city_codes = None

    def get_destination_data(self) -> list:
        """Return a data list of the cities in the sheet."""
        response = requests.get(
            url=SHEETY_FLIGHTDEALS_ENDPOINT,
            headers=SHEETY_HEADERS,
            timeout=10,
        )
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self) -> None:
        """Update the city's IATA code in the table."""
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"],
                },
            }
            response = requests.put(
                url=f"{SHEETY_FLIGHTDEALS_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=SHEETY_HEADERS,
                timeout=10,
            )
            print(response.text)

    def get_customer_emails(self) -> list:
        """Return the emails from the customers."""
        response = requests.get(
            url=SHEETY_FLIGHTDEALS_USERS_ENDPOINT,
            headers=SHEETY_HEADERS,
            timeout=10,
        )
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data


def notification_manager(message: str) -> None:
    """Send the notifications with the deal flight details.
    
    Since we are not using Twilio for the sending SMS functionality, we will
    just print out the results passed to this function.
    """
    print("Sending SMS...")
    print(message)


def post_new_user(first_name: str, last_name: str, email: str) -> None:
    """Add a new user to the users table."""
    new_header = {
        "Authorization": f"Bearer {os.getenv("SHEETY_FLIGHTDEALS_TOEKN")}",
        "Content-Type": "application/json",
    }
    body = {
        "user": {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
        }
    }
    response = requests.post(
        url=SHEETY_FLIGHTDEALS_USERS_ENDPOINT,
        headers=new_header,
        json=body,
        timeout=10,
    )
    response.raise_for_status()
    print(response.text)


def input_new_user() -> None:
    """Get inputs from the user to post new user."""
    print("Welcome to The Flight Club.\n"
          "We find the best flight deals and email them to you.")

    first_name = input("What is your first name? ").title()
    last_name = input("What is your last name? ").title()

    email1 = "email1"
    email2 = "email2"
    while email1 != email2:
        email1 = input("What is your email? ")
        if email1.lower() == "quit" or email1.lower() == "exit":
            sys.exit(0)
        email2 = input("Confirm your email: ")
        if email2.lower() == "quit" or email2.lower() == "exit":
            sys.exit(0)
    print("Confirmed! You're in the club!")
    post_new_user(first_name=first_name, last_name=last_name, email=email1)


def main():
    """Run the main code."""
    data_manager = DataManager()
    flight_search = FlightSearch()
    sheet_data = data_manager.get_destination_data()

    # If there's a city without its IATA code, get the code and put in the table
    if sheet_data[0]["iataCode"] == "":
        city_names = [row["city"] for row in sheet_data]
        data_manager.city_codes = flight_search.get_destination_code(city_names)
        data_manager.update_destination_codes()
        sheet_data = data_manager.get_destination_data()

    # Make a dictionary with all cities in the table
    destinations = {
        data["iataCode"]: {
            "id": data["id"],
            "city": data["city"],
            "price": data["lowestPrice"]
        } for data in sheet_data
    }

    # Get the dates for flight search
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    six_month_from_today = datetime.datetime.now() + datetime.timedelta(days=6*30)

    # Search each flight destination
    for destination_code in destinations:
        flight = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination_code,
            from_time=tomorrow,
            to_time=six_month_from_today,
        )
        if flight is None:
            continue

        if flight.price < destinations[destination_code]["price"]:
            notification_manager(message=f"Low price alert! Only R${flight.price}!"
                                 f"To fly from {flight.origin_city}-{flight.origin_airport}"
                                 f"to {flight.destination_city}-{flight.destination_airport},"
                                 f"from {flight.out_date} to {flight.return_date}"
                                 )
            if flight.stop_overs > 0:
                notification_manager(message=f"\nFlight has {flight.stop_overs} stop over,"
                                     f"via {flight.via_city}")

    # Register new user
    # input_new_user()


if __name__ == "__main__":
    main()

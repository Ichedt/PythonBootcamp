"""
Day 39 - Cheap Flight Finder

tags: capstone project
"""
import datetime
import os
from dotenv import load_dotenv
import requests

load_dotenv()

SHEETY_FLIGHTDEALS_ENDPOINT = os.getenv("SHEETY_FLIGHTDEALS_ENDPOINT")
SHEETY_FLIGHTDEALS_TOKEN = os.getenv("SHEETY_FLIGHTDEALS_TOKEN")
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
        price,
        origin_city: str,
        origin_airport: str,
        destination_city: str,
        destination_airport: str,
        out_date: str,
        return_date: str,
    ):
        """Construct all the flight data necessary for the search."""
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date


class FlightSearch:
    """Class responsible for handling the Flight Search API."""

    def get_destination_code(self, city_name: str) -> str:
        """Gets the IATA code for the given city."""
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
        """Return a FlightData object with information about the flights."""
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
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
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0],
        )
        print(f"{flight_data.destination_city}: R$ {flight_data.price}")
        return flight_data


class DataManager:
    """Class responsible for handling the data table."""

    def __init__(self):
        """Construct the dictionary for the destination data."""
        self.destination_data = {}

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


def notification_manager(message: str) -> None:
    """Send the notifications with the deal flight details.
    
    Since we are not using Twilio for the sending SMS functionality, we will
    just print out the results passed to this function.
    """
    print("Sending SMS...")
    print(message)


def main():
    """Run the code."""
    data_manager = DataManager()
    sheet_data = data_manager.get_destination_data()
    flight_search = FlightSearch()
    if sheet_data[0]["iataCode"] == "":
        for row in sheet_data:
            row["iataCode"] = flight_search.get_destination_code(row["city"])
        data_manager.destination_data = sheet_data
        data_manager.update_destination_codes()

    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    six_month_from_today = datetime.datetime.now() + datetime.timedelta(days=6*30)
    for destination in sheet_data:
        flight = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today,
        )
        if flight.price < destination["lowestPrice"]:
            # String reduced.
            notification_manager(message=f"Low price alert! Only R${flight.price}!")


if __name__ == "__main__":
    main()

import sys
import logging
from typing import Optional, Tuple
from datetime import datetime
import requests
import pytz
import openmeteo_requests
import requests_cache
from retry_requests import retry

# Logging configuration

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Variables
CITY_OF_INTEREST = "Cordoba"
COUNTRY_CODE = "AR"
GEOCODING_URL = "http://geocoding-api.open-meteo.com/v1/search"


# Setting Open Meteo Session
cache_session = requests_cache.CachedSession(".cache", expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def get_lat_long(city: str, country_code: str) -> Optional[Tuple[float, float]]:
    """This function returns the latitude for city and country code entered

    Args:
        city (str): city name
        country_code (str): country code in ISO 3166-1 format

    Returns:
        Optional[Tuple[float,float]]: latitude, longitude
    """

    # Paramos for the endpoint
    params = {"name": city, "countrCode": country_code, "count": 1}

    # Request data
    try:
        logging.info("Requesting data")
        city_data = requests.get(url=GEOCODING_URL, params=params, timeout=20)

    except requests.exceptions.MissingSchema as ms_error:
        logging.error("Bad URL")
        raise ms_error

    except requests.exceptions.ConnectionError as c_error:
        logging.error("ConnectionError")
        logging.error("Check if URL is correct")
        raise c_error

    # Catch any other exceptions, get error message and type to add later the specific exception
    except Exception as e:
        logging.error("Unexpected Error")
        logging.error(type(e))
        raise e

    # Get status code and parse data
    request_status = city_data.status_code

    match request_status:
        # Request Okey
        case 200:
            json_data = city_data.json()
            logging.debug("Data: %s", json_data)
            # Save latitude
            latitude = json_data["results"][0]["latitude"]
            logging.debug("latitude: %s", latitude)
            # Save longitude
            longitude = json_data["results"][0]["longitude"]
            logging.debug("longitude: %s", longitude)

            # Return values
            return latitude, longitude

        case 400:
            logging.error(city_data.json())
            logging.error(
                "Bad Request (Status 400), check imput parameters. "
                'Example format:{"name": "Cordoba", "countrCode": "AR", "count": 1}'
            )
            sys.exit(1)

        # Handle any other case
        case _:
            logging.error(city_data.json())
            logging.error("Bad Request, add new case with all necessary details")
            sys.exit(1)


## Main program
if __name__ == "__main__":

    # Get latitude and longitude

    lat, long = get_lat_long(city=CITY_OF_INTEREST, country_code=COUNTRY_CODE)

    # Get current weather data
    # API url for current weather values
    URL = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}1&longitude={long}&current=temperature_2m"
    )

    try:
        logging.info("Requesting data")
        # Request to the endpoint
        data = requests.get(
            url=URL,
            timeout=10,
        )
    except requests.exceptions.ConnectionError as CError:
        logging.error(CError)
        sys.exit(1)

    logging.info("Data retrieved")

    logging.info("Extractin data from json")

    logging.debug(data.json())
    current_temperature = data.json()["current"]["temperature_2m"]
    current_time_str = data.json()["current"]["time"]
    utc_dt = datetime.fromisoformat(current_time_str).replace(tzinfo=pytz.utc)
    argentina_timezone = pytz.timezone("America/Argentina/Buenos_Aires")
    argentina_dt = utc_dt.astimezone(argentina_timezone)

    logging.info("Data parsed...")

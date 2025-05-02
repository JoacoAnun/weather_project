import requests
import logging
from typing import Optional, Tuple

import openmeteo_requests
import requests_cache
import pandas as pd
import numpy as np
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

# API url for weather values
url = "http://archive-api.open-meteo.com/v1/archive"


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
        city_data = requests.get(url=GEOCODING_URL, params=params)

    except requests.exceptions.MissingSchema as MSError:
        logging.error("Bad URL")
        raise MSError

    except requests.exceptions.ConnectionError as CError:
        logging.error("ConnectionError")
        logging.error("Check if URL is correct")
        raise CError

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
            logging.debug(f"Data: {json_data}")
            # Save latitude
            latitude = json_data["results"][0]["latitude"]
            logging.debug(f"latitude: {latitude}")
            # Save longitude
            longitude = json_data["results"][0]["longitude"]
            logging.debug(f"longitude: {longitude}")

            # Return values
            return latitude, longitude

        case 400:
            logging.error(city_data.json())
            logging.error(
                'Bad Request (Status 400), check imput parameters. Example format:{"name": "Cordoba", "countrCode": "AR", "count": 1}'
            )
            raise Exception("Bad Request (Status 400)")

        # Handle any other case
        case _:
            logging.error(city_data.json())
            logging.error("Bad Request, add new case with all necessary details")
            raise Exception("Bad Request")


## Main program
if __name__ == "__main__":

    # Get latitude and longitude

    latitude, longitude = get_lat_long(city=CITY_OF_INTEREST, country_code=COUNTRY_CODE)

    # Get weather data
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": "2000-01-01",
        "end_date": "2000-01-02",
        "hourly": "temperature_2m",
    }

    # Data is retrieved as a list of the locations sets in params
    responses = openmeteo.weather_api(url=url, params=params)

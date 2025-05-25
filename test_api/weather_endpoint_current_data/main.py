"""Testing the Open Meteo API for current weather data."""

import sys
import logging
import requests

# Logging configuration
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

URL = (
    "https://api.open-meteo.com/v1/forecast?"
    "latitude=-31.41&longitude=-64.18&current=temperature_2m"
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

logging.debug(data.json())

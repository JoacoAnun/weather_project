"""Get geocoding data for a specific location using Open Meteo API."""

import sys
import logging
import requests

# Logging configuration
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    logging.info("Requesting data")
    # Request to the endpoint
    data = requests.get(
        url=(
            "https://geocoding-api.open-meteo.com/v1/search"
            "?name=Cordoba&count=1&language=en&format=json&countryCode=AR"
        ),
        timeout=10,
    )

except requests.exceptions.ConnectionError as CError:
    logging.error(CError)
    sys.exit(1)

logging.info("Data retrieved")

print(data.json())

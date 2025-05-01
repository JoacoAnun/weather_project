import openmeteo_requests
import requests_cache
import pandas as pd
import numpy as np
from retry_requests import retry


# Setting Open Meteo Session

cache_session = requests_cache.CachedSession(".cache", expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


# API url
url = "http://archive-api.open-meteo.com/v1/archive"

# Try for cordoba Argentina lat and long
# For multiple locations add a list in lat and long
params = {
    "latitude": -31.42,
    "longitude": -64.18,
    "start_date": "2000-01-01",
    "end_date": "2009-12-31",
    "hourly": "temperature_2m",
}

# Data is retrieved as a list of the locations sets in params
responses = openmeteo.weather_api(url=url, params=params)

# First response
response = responses[0]

# Fetching data
elevation = response.Elevation()
print(f"Elevation (m) = {elevation}")


hourly = response.Hourly()

# Time is return in Epoch (need to convert to datetime)
print(pd.to_datetime(hourly.Time(), unit="s", utc=True))
print(pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True))

# Use pandas to create time series
start_time = pd.to_datetime(hourly.Time(), unit="s", utc=True)
end_time = pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True)


# Parse data to a dictionary before loading into a pandas dataframe
hourly_data = {
    "date": pd.date_range(
        start=start_time,
        end=end_time,
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left",
    )
}


# Extract temperature (celsius)
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
# Add temperature to hourly_data dictionary
hourly_data["temperature_2m"] = hourly_temperature_2m


# Create and print dataframe
hourly_dataframe = pd.DataFrame(data=hourly_data)
print(hourly_dataframe)

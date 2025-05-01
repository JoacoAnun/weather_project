# Hitroical Endpoint

- Historical Data URL: https://open-meteo.com/en/docs/historical-weather-api

## Request URL

http://archive-api.open-meteo.com/v1/archive

## Json example for payload

```json
{
    "latitude": -31.42,
    "longitude": -64.18,
    "start_date": "2000-01-01",
    "end_date": "2009-12-31",
    "hourly": "temperature_2m",
}
```

For more parameters check the API docs
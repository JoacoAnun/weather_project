# Geocoding Endpoint

- Request example URL: https://geocoding-api.open-meteo.com/v1/search?name=Cordoba&count=1&language=en&format=json

- Example response:
```json
{
"results": [
    {
        "id": 3860259,
        "name": "Córdoba",
        "latitude": -31.4135,
        "longitude": -64.18105,
        "elevation": 395,
        "feature_code": "PPLA",
        "country_code": "AR",
        "admin1_id": 3860255,
        "timezone": "America/Argentina/Cordoba",
        "population": 1428214,
        "country_id": 3865483,
        "country": "Argentina",
        "admin1": "Cordoba"
    }
        ],
    "generationtime_ms": 1.314044
}
```
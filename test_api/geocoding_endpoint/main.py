import requests


# Request to the endpoint
# Added country code for more specific location, if using only Cordoba for example and count > 1, it brings also Cordova from Span and other
data = requests.get(
    url="https://geocoding-api.open-meteo.com/v1/search?name=Cordoba&count=1&language=en&format=json&countryCode=AR"
)

# Print data if status code of get request = 200 OK
if data.status_code == 200:
    print(data.json())

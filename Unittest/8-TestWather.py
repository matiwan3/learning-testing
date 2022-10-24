import requests


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
API = BASE_URL + "?q={city_name}&appid={api_key}&units=metric"
def find_weather(city: str) -> dict:
    """Queries the weather API and returns the weather data for a particular city."""
    url = API.format(vity_name = city, api_key=API_KEY)
    resp = requests.get(url)
    return resp.json()
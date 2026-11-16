import logging
import requests

logger = logging.getLogger(__name__)
API_URL = "https://api.open-meteo.com/v1/forecast"
VARIABLES = ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"]

def fetch_weather(city, session=None):
    client = session or requests.Session()
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "hourly": ",".join(VARIABLES),
        "forecast_days": 1,
        "timezone": "UTC",
    }
    response = client.get(API_URL, params=params, timeout=20)
    response.raise_for_status()
    payload = response.json()
    payload["city"] = city["city"]
    logger.info("Fetched payload for %s", city["city"])
    return payload

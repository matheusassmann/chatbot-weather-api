# chatbot/weather_service.py
import requests
from datetime import datetime, timedelta, timezone

def get_forecast(city: str) -> dict:
    # Geocodifica a cidade
    geo_resp = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city}
    ).json()

    if not geo_resp.get("results"):
        return {"error": "Cidade não encontrada"}

    location = geo_resp["results"][0]
    lat, lon = location["latitude"], location["longitude"]

    # Data de amanhã no formato ISO
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date().isoformat()

    # Obtém a previsão
    forecast_resp = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_min,temperature_2m_max",
            "timezone": "auto",
            "start_date": tomorrow,
            "end_date": tomorrow
        }
    ).json()

    temps = forecast_resp.get("daily", {})
    return {
        "min": temps.get("temperature_2m_min", [None])[0],
        "max": temps.get("temperature_2m_max", [None])[0],
        "date": tomorrow
    }
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Mumbai"


def normalize_weather(condition):
    condition = condition.lower()

    if "rain" in condition:
        return "rainy"
    elif "cloud" in condition:
        return "cloudy"
    elif "clear" in condition:
        return "sunny"
    elif "haze" in condition or "mist" in condition:
        return "hazy"
    else:
        return "normal"


def get_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        temperature = data["main"]["temp"]
        weather_main = data["weather"][0]["main"]

        return {
            "city": CITY,
            "temperature": temperature,
            "weather": weather_main,
            "weather_type": normalize_weather(weather_main)
        }

    except Exception:
        # Fallback if API fails
        return {
            "city": CITY,
            "temperature": 30,
            "weather": "Clear",
            "weather_type": "sunny"
        }

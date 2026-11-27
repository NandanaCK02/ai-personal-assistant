
import requests


def get_weather(city: str):

    # Step 1: Get city coordinates
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    geo_response = requests.get(
        geo_url,
        params=geo_params,
        timeout=10
    )

    geo_response.raise_for_status()

    geo_data = geo_response.json()

    if not geo_data.get("results"):
        return {"error": f"City '{city}' not found"}

    location = geo_data["results"][0]

    latitude = location["latitude"]
    longitude = location["longitude"]

    # Step 2: Get weather information
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
        "timezone": "auto"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params,
        timeout=10
    )

    weather_response.raise_for_status()

    weather_data = weather_response.json()

    # Step 3: Return selected weather details
    current = weather_data["current"]

    return {
        "city": location["name"],
        "country": location.get("country"),
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "weather_code": current["weather_code"],
        "time": current["time"]
    }


# Test the function
if __name__ == "__main__":
    result = get_weather("Kozhikode")
    print(result)

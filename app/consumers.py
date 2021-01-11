from weather_app.helpers import get_env_value
import httpx


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
OPEN_WEATHER_API_KEY = get_env_value("OPEN_WEATHER_API_KEY")

def _built_url_for_call(city_name):
    return f"{BASE_URL}?q={city_name}&appid={OPEN_WEATHER_API_KEY}&units=metric"

async def get_weather_for_city(city_name):
    async with httpx.AsyncClient() as client:
        response = await client.get(_built_url_for_call(city_name))
        return response.json()
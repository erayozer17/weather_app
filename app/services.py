from django.http import Http404, HttpResponseServerError

from .consumers import get_weather_for_city
from .helpers import get_cache_or_call


async def get_json_for_the_city(city_name):
    try:
        result = await get_cache_or_call(city_name, get_weather_for_city, city_name)
        return {
            "city": city_name,
            "temp": result["main"]["temp"],
            "temp_min": result["main"]["temp_min"],
            "temp_max": result["main"]["temp_max"],
            "pressure": result["main"]["pressure"],
            "humidity": result["main"]["humidity"],
            "wind_speed": result["wind"]["speed"],
            "wind_direction": _get_wind_direction(result["wind"]["deg"]),
            "description": result["weather"][0]["description"].capitalize()
        }
    except KeyError:
        raise Http404("Requested city not found.")
    except Exception:
        raise HttpResponseServerError()


def _get_wind_direction(degree):
    if degree >= 360:
        degree = degree % 360
    directions = ["N", "E", "E", "S", "S", "W", "W", "N"]
    direction = degree // 45
    return directions[direction]

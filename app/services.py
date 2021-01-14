from django.http import Http404, HttpResponseServerError

from .consumers import get_weather_for_city
from .helpers import get_cache_or_call
from .models import WeatherResult


async def get_json_for_the_city(city_name):
    try:
        result = await get_cache_or_call(city_name, get_weather_for_city, city_name)
        return WeatherResult.get_weather_result(result)
    except KeyError:
        raise Http404("Requested city not found.")
    except Exception:
        raise HttpResponseServerError()

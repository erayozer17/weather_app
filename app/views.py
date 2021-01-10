from django.shortcuts import render
from django.core.cache import cache

from .services import get_json_for_the_city
from .forms import CityForm
from .helpers import get_env_value

def get_current_weather_in_city(request):
    if request.POST:
        form = CityForm(request.POST)
        city_name = form["name"].value()
        cache_key = city_name.lower()
        cache_time = get_env_value("CACHING_TIME")
        result = cache.get(city_name.lower())
        if not result:
            result = get_json_for_the_city(city_name)
            cache.set(cache_key, result, int(cache_time))
        return render(request, "weather_forecast.html", {"result": result, "form": form})
    else:
        form = CityForm()
        return render(request, "weather_forecast.html", {"form": form})

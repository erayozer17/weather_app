from django.shortcuts import render

from .services import get_json_for_the_city
from .forms import CityForm

def get_current_weather_in_city(request):
    if request.POST:
        form = CityForm(request.POST)
        city_name = form["name"].value()
        result = get_json_for_the_city(city_name)
        return render(request, "weather_forecast.html", {"result": result, "form": form})
    else:
        form = CityForm()
        return render(request, "weather_forecast.html", {"form": form})

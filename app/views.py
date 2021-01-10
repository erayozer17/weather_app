from django.shortcuts import render

from .services import get_weather_for_city

def get_current_weather_in_city(request):
    if request.POST:
        city_name = request.POST["city_name"]
        result = get_weather_for_city(city_name)
        return render(request, 'weather_forecast.html', {"result": result})

from django.shortcuts import render

from .services import get_json_for_the_city
from .forms import CityForm


async def get_current_weather_in_city(request):
    if request.POST:
        form = CityForm(request.POST)
        city_name = form["name"].value()
        result = await get_json_for_the_city(city_name)
        return render(request, "weather_forecast.html", {"result": result, "form": form})
    else:
        form = CityForm()
        return render(request, "weather_forecast.html", {"form": form})


def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {"message": exception})


def custom_error_view(request, exception=None):
    return render(request, "errors/500.html", {"message": exception})


def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", {"message": exception})


def custom_bad_request_view(request, exception=None):
    return render(request, "errors/400.html", {"message": exception})

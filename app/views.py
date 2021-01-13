from django.shortcuts import render
from django.core.exceptions import SuspiciousOperation

from .services import get_json_for_the_city
from .forms import CityForm


async def get_current_weather_in_city(request):
    if request.POST:
        form = CityForm(request.POST)
        if(not form.is_valid()):
            raise SuspiciousOperation("name field cannot be empty.")
        city_name = form.cleaned_data["name"]
        result = await get_json_for_the_city(city_name)
        return render(request, "weather_forecast.html", {"result": result, "form": form})
    else:
        form = CityForm()
        return render(request, "weather_forecast.html", {"form": form})


def custom_page_not_found_view(request, exception):
    response = render(request, "errors/404.html", {"message": exception})
    response.status_code = 404
    return response


def custom_error_view(request, exception=None):
    response = render(request, "errors/500.html", {"message": exception})
    response.status_code = 500
    return response


def custom_permission_denied_view(request, exception=None):
    response = render(request, "errors/403.html", {"message": exception})
    response.status_code = 403
    return response


def custom_bad_request_view(request, exception=None):
    response = render(request, "errors/400.html", {"message": exception})
    response.status_code = 400
    return response

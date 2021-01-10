from django.urls import path
from .views import get_current_weather_in_city

urlpatterns = [
    path('', get_current_weather_in_city, name='get_current_weather_in_city')
]

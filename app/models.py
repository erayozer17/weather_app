from django.db import models
from django.utils.translation import ugettext_lazy as _


class City(models.Model):
    name = models.CharField(_("City Name"), max_length=50)


class WeatherResult:

    def __init__(self, city, temp, temp_min, temp_max, pressure, humidity, wind_speed, wind_direction, description):
        self.city = city
        self.temp = temp
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.pressure = pressure
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.description = description

    @classmethod
    def get_weather_result(cls, json):
        return cls(
            json["name"],
            json["main"]["temp"],
            json["main"]["temp_min"],
            json["main"]["temp_max"],
            json["main"]["pressure"],
            json["main"]["humidity"],
            json["wind"]["speed"],
            cls.get_wind_direction(json["wind"]["deg"]),
            json["weather"][0]["description"].capitalize()
        )

    @staticmethod
    def get_wind_direction(degree):
        if degree >= 360:
            degree = degree % 360
        directions = ["N", "E", "E", "S", "S", "W", "W", "N"]
        direction = degree // 45
        return directions[direction]

    def __eq__(self, obj):
        return (
            self.city == obj.city and
            self.temp == obj.temp and
            self.temp_min == obj.temp_min and
            self.temp_max == obj.temp_max and
            self.pressure == obj.pressure and
            self.humidity == obj.humidity and
            self.wind_speed == obj.wind_speed and
            self.wind_direction == obj.wind_direction and
            self.description == obj.description
        )

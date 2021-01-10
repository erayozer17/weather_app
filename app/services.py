from .consumers import get_weather_for_city


def get_json_for_the_city(city_name):
    raw_result = get_weather_for_city(city_name)
    return {
        "city": city_name,
        "temp_min": raw_result["main"]["temp_min"],
        "temp_max": raw_result["main"]["temp_max"],
        "pressure": raw_result["main"]["pressure"],
        "humidity": raw_result["main"]["humidity"],
        "wind_speed": raw_result["wind"]["speed"],
        "wind_direction": _get_wind_direction(raw_result["wind"]["deg"]),
        "description": raw_result["weather"]["description"]
    }

def _get_wind_direction(degree):
    if degree > 360:
        degree = degree % 360
    directions = ["N", "E", "E", "S", "S", "W", "W", "N"]
    direction = degree // 45
    return directions[direction]

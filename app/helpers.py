from django.core.exceptions import ImproperlyConfigured
from django.core.cache import cache

from weather_project.helpers import get_env_value


def get_caching_time():
    coefficient = 60
    posibble_values = [0, 1, 2]
    caching_times = [5, 10, 60]
    try:
        environ_value = int(get_env_value("CACHING_TIME"))
    except ValueError:
        raise ImproperlyConfigured("CACHING_TIME should be integer.")
    if environ_value not in posibble_values:
        error_msg = "CACHING_TIME should be in {}".format(posibble_values)
        raise ImproperlyConfigured(error_msg)
    return caching_times[environ_value] * coefficient


async def get_cache_or_call(cache_key, func, *args):
    cache_key = cache_key.replace(" ", "_")
    cache_key = cache_key.lower()
    cache_time = get_caching_time()
    result = cache.get(cache_key)
    if not result:
        result = await func(*args)
        cache.set(cache_key, result, cache_time)
    return result


def get_wind_direction(degree):
    if degree >= 360:
        degree = degree % 360
    directions = ["N", "E", "E", "S", "S", "W", "W", "N"]
    direction = degree // 45
    return directions[direction]

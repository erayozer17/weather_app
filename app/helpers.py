from django.core.exceptions import ImproperlyConfigured
from django.core.cache import cache

from weather_app.helpers import get_env_value


def _get_caching_time():
    coefficient = 60
    posibble_values = [0, 1, 2]
    caching_times = [5, 10, 60]
    environ_value = int(get_env_value("CACHING_TIME"))
    if environ_value not in posibble_values:
        error_msg = "CACHING_TIME should be in {}".format(posibble_values)
        raise ImproperlyConfigured(error_msg)
    return caching_times[environ_value] * coefficient


def get_cache_or_call(cache_key, func, *args):
    cache_key = cache_key.lower()
    cache_time = _get_caching_time()
    result = cache.get(cache_key)
    if not result:
        result = func(*args)
        cache.set(cache_key, result, cache_time)
    return result
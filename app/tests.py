import asyncio
import unittest
from unittest import mock
from parameterized import parameterized
import os

from django.test import SimpleTestCase, override_settings
from django.urls import reverse
from django.core.exceptions import ImproperlyConfigured
from django.core.cache import cache
from freezegun import freeze_time

from .forms import CityForm
from .services import get_json_for_the_city
from .helpers import get_caching_time, get_cache_or_call
from .models import WeatherResult


class Helpers:
    @staticmethod
    def _run(coro):
        return asyncio.get_event_loop().run_until_complete(coro)

    @staticmethod
    def asyncMock(*args, **kwargs):
        m = mock.MagicMock(*args, **kwargs)

        async def mock_coro(*args, **kwargs):
            return m(*args, **kwargs)

        mock_coro.mock = m
        return mock_coro


class TestForm(unittest.TestCase):

    def test_valid_form(self):
        data = {'name': 'Cologne'}
        form = CityForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'name': ''}
        form = CityForm(data=data)
        self.assertFalse(form.is_valid())


class TestView(SimpleTestCase):

    def test_get_request_on_get_current_weather_in_city(self):
        url = reverse("get_current_weather_in_city")
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'weather_forecast.html')
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIsInstance(form, CityForm)
        self.assertIn('form', response.context)

    def mock_get_json_for_the_city(*args, **kwargs):
        return {"mocked": "mocked_value"}

    @mock.patch("app.views.get_json_for_the_city", side_effect=mock_get_json_for_the_city)
    def test_post_request_on_get_current_weather_in_city(self, mock_get):
        url = reverse("get_current_weather_in_city")
        response = self.client.post(url, data={"name": "Cologne"})
        self.assertTemplateUsed(response, 'weather_forecast.html')
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertIsInstance(form, CityForm)
        self.assertIn('result', response.context)
        self.assertIn('form', response.context)
        self.assertEquals(response.context['result']['mocked'], 'mocked_value')

    @mock.patch("app.views.get_json_for_the_city", side_effect=mock_get_json_for_the_city)
    def test_post_invalid_request_on_get_current_weather_in_city(self, mock_get):
        url = reverse("get_current_weather_in_city")
        response = self.client.post(url, data={"name": ""})
        self.assertEqual(response.status_code, 400)


class TestService(unittest.TestCase):

    expected_result_from_api = {
        "weather": [
            {
                "description": "clear sky",
            }
        ],
        "main": {
            "temp": 282.55,
            "temp_min": 280.37,
            "temp_max": 284.26,
            "pressure": 1023,
            "humidity": 100
        },
        "wind": {
            "speed": 1.5,
            "deg": 350
        },
        "name": "Cologne",
    }

    @mock.patch("app.services.get_cache_or_call", new=Helpers.asyncMock(return_value=expected_result_from_api))
    def test_get_json_for_the_city(self):
        res = Helpers._run(get_json_for_the_city("Cologne"))
        expected = WeatherResult(
            "Cologne",
            282.55,
            280.37,
            284.26,
            1023,
            100,
            1.5,
            "N",
            "Clear sky"
        )
        assert(res == expected)


class TestHelpers(unittest.TestCase):

    def test_get_caching_time(self):
        os.environ["CACHING_TIME"] = "0"
        self.assertEqual(get_caching_time(), 5*60)
        os.environ["CACHING_TIME"] = "1"
        self.assertEqual(get_caching_time(), 10*60)
        os.environ["CACHING_TIME"] = "2"
        self.assertEqual(get_caching_time(), 60*60)
        os.environ["CACHING_TIME"] = "a"
        self.assertRaises(ImproperlyConfigured, get_caching_time)
        os.environ["CACHING_TIME"] = "3"
        self.assertRaises(ImproperlyConfigured, get_caching_time)

    @override_settings(
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'test-cache'}
            }
        )
    @mock.patch("django.core.cache.cache.set")
    def test_get_cache_when_not_expired(self, mock):
        mock_get_weather_for_city = {"mocked": "mocked_value"}
        os.environ["CACHING_TIME"] = "0"
        with freeze_time("2021-01-14 12:00:01"):
            cache.set("key", mock_get_weather_for_city, 300)
        with freeze_time("2021-01-14 12:05:00"):
            get_cache_or_call("key", lambda x: x, "key")
            mock.assert_called_once()


class TestModels(unittest.TestCase):
    @parameterized.expand([
        [0, "N"], [23, "N"],
        [45, "E"], [95, "E"],
        [180, "S"], [224, "S"],
        [285, "W"], [234, "W"],
        [324, "N"], [360, "N"],
        [410, "E"], [560, "S"],
    ])
    def test_get_wind_direction(self, degree, expected):
        self.assertEqual(WeatherResult.get_wind_direction(degree), expected)

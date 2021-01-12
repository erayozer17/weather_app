import asyncio
import unittest
from unittest import mock

from django.test import SimpleTestCase
from django.urls import reverse

from .forms import CityForm
from .services import get_json_for_the_city


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
    }

    def _run(self, coro):
        return asyncio.get_event_loop().run_until_complete(coro)

    def AsyncMock(*args, **kwargs):
        m = mock.MagicMock(*args, **kwargs)

        async def mock_coro(*args, **kwargs):
            return m(*args, **kwargs)

        mock_coro.mock = m
        return mock_coro

    @mock.patch("app.services.get_cache_or_call", new=AsyncMock(return_value=expected_result_from_api))
    def test_get_json_for_the_city(self):
        res = self._run(get_json_for_the_city("Cologne"))
        expected = {
            "city": "Cologne",
            "temp": 282.55,
            "temp_min": 280.37,
            "temp_max": 284.26,
            "pressure": 1023,
            "humidity": 100,
            "wind_speed": 1.5,
            "wind_direction": "N",
            "description": "Clear sky"
        }
        self.assertEqual(res, expected)

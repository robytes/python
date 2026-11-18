
import unittest
from io import StringIO
from contextlib import redirect_stdout

from weather import display_forecast


class TestWeather(unittest.TestCase):

    def test_display_forecast(self):
        forecast_periods = [
            {
                "name": "Tonight",
                "temp": 45,
                "temp_unit": "F",
                "short_forecast": "Mostly Cloudy"
            }
        ]

        expected_output = "Tonight: 45°F - Mostly Cloudy\n"

        output = StringIO()

        with redirect_stdout(output):
            display_forecast(forecast_periods)

        actual_output = output.getvalue()

        self.assertEqual(actual_output, expected_output)


if __name__ == "__main__":
    unittest.main()

    # def test_get_forecast(self):
    #     forecast_url = "https://example.com/forecast"
    #     headers = {"User-Agent": "WeatherPractice/1.0"}

    #     with patch("weather.requests.get") as mock_get:

# Latitude: 47.6512744° N (or 47° 39' 05" N)
# Longitude: -122.3507443° W (or 122° 21' 04" W)
import requests


def get_forecast_url(lat, long, headers):

    nws_points_url = "https://api.weather.gov/points/"
    nws_full_url = nws_points_url + str(lat) + "," + str(long)
    
    r = requests.get(
        nws_full_url,
        headers=headers,
        timeout=10
        )
    r.raise_for_status()

    weather_data = r.json()
    nws_forecast_url = weather_data["properties"]["forecast"]

    return nws_forecast_url

def get_forecast(forecast_url, headers):

    forecast_response = requests.get(
        forecast_url,
        headers=headers,
        timeout=10
    )
    
    forecast_response.raise_for_status()
    forecast_data = forecast_response.json()

    forecast_periods = []

    for period in forecast_data["properties"]["periods"]:
        forecast_period = {
            "name": period["name"],
            "temp": period["temperature"],
            "temp_unit": period["temperatureUnit"],
            "short_forecast": period["shortForecast"]
        }
        forecast_periods.append(forecast_period)

    return forecast_periods

def display_forecast(forecast_periods):
    for period in forecast_periods:
        print(f"{period["name"]}: {period["temp"]}°{period["temp_unit"]} - {period["short_forecast"]}")

def main():    
    lat = 47.6512
    long = -122.3507
    headers = {"User-Agent": "WeatherPractice/1.0 (robert.mullen451@gmail.com)"}
    try:
        forecast_url = get_forecast_url(lat, long, headers)
        forecast_periods = get_forecast(forecast_url, headers)
        display_forecast(forecast_periods)
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"NWS API request failed: {e}")
        
if __name__ == "__main__":
    main()
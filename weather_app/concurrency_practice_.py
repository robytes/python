import time
from concurrent.futures import ThreadPoolExecutor

def fetch_weather(city, delay):
    print(f"Starting request for {city}")
    time.sleep(delay)
    print(f"Finished request for {city}")
    return f"{city}: Forecast retrieved"

cities = ["Seattle", "Portland", "Spokane"]
delays = [3, 1, 2]

with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(fetch_weather, cities, delays)

    for result in results:
        print(result)
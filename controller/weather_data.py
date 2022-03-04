import itertools
import os
from multiprocessing import Pool

from config import config_execution
from entity.open_weather_map import get_url
from repository.weather_requester import get_weather_data


def gather_weather_data():
    api_key = config_execution.get_api_key()
    dates = config_execution.get_last_5_dates()
    cities = config_execution.get_cities()

    cities_requests = [{**city, "api_key": api_key} for city in cities]
    dates_to_requests = [{"date_ts": temp_date} for temp_date in dates]

    # cartesian product
    complete_request = list(itertools.product(cities_requests, dates_to_requests))

    complete_request = [{**item[0], **item[1]} for item in complete_request]
    with Pool(os.cpu_count()) as pool:
        weather_data = pool.map(perform_weather_request, complete_request)

    return weather_data


def perform_weather_request(city_request):
    url_to_request = get_url(**city_request)
    return get_weather_data(url_to_request)



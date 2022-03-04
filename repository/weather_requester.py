import logging

import requests


def get_weather_data(url: str):
    output = requests.get(url)

    if not output.ok:
        logging.warning("Request found a problem and no data gathered")
        return None
    return output.json()

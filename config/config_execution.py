from datetime import datetime, timedelta
import logging
import os

import yaml
import importlib.resources


def get_cities():
    yaml_content = load_yaml_content()
    return yaml_content["sources"]["cities"]


def get_sink_path(step_name: str):
    yaml_content = load_yaml_content()
    return yaml_content["sinks"][step_name]["sink_path"]


def load_yaml_content():
    config = importlib.resources.open_binary("config", "config.yaml")
    return yaml.load(config, Loader=yaml.FullLoader)


def get_last_5_dates():
    date_to_execute = get_date()
    return [int((date_to_execute - timedelta(index)).timestamp()) for index in range(0, 5)]


def get_date():
    date_to_execute = os.getenv("DATE_TO_RUN", None)
    if date_to_execute is not None:
        try:
            logging.info("Date to execute informed: ", date_to_execute)
            return datetime.strptime(date_to_execute, "%Y-%m-%d")
        except Exception as error:
            logging.error("An error occurred: ", str(error))
    date_now = datetime.now()
    logging.info("No correct date was informed, date to be used: ", date_now)
    return date_now


def get_api_key():
    api_key = load_yaml_content()["env"]["api"]
    if api_key is None:
        logging.error("Please, an API_KEY env Needs to be defined in config.yaml")
        raise Exception("Missing API_KEY ENV")
    return api_key

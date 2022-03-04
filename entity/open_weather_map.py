URL = (
    "http://api.openweathermap.org/data/2.5/onecall/timemachine?"
    "lat={lat}&"
    "lon={lon}&"
    "dt={date_ts}&"
    "appid={api_key}"
)


def get_url(**kwargs):
    return URL.format_map(kwargs)

from datetime import datetime
from data.spec import specification

import pytz


TIMEZONE = "Europe/Moscow"
TIMEFORMAT = "%d/%m/%Y %H:%M:%S"

def get_current_time(time_form=TIMEFORMAT):
    try:
        tz = pytz.timezone(TIMEZONE)
        localized_time = datetime.now(tz)
        return localized_time.strftime(time_form)
    except pytz.UnknownTimeZoneError:
        print(f"Unknown time zone: {TIMEZONE}")
        return None
    

def is_delivery_day(date)->bool:
    day = date.split(".")[0]
    div = specification["day_frequence"]

    return day % div == 0

from datetime import datetime, timedelta
from data.spec import specification

import pytz


TIMEZONE = "Europe/Moscow"
TIMEFORMAT = "%d/%m/%Y"

def get_current_time(time_form=TIMEFORMAT):
    try:
        tz = pytz.timezone(TIMEZONE)
        localized_time = datetime.now(tz)
        return localized_time.strftime(time_form)
    except pytz.UnknownTimeZoneError:
        print(f"Unknown time zone: {TIMEZONE}")
        return None
    
def convert_date(timestamp):
    return datetime.fromtimestamp(timestamp, pytz.timezone(TIMEZONE))

def increase_date(dt, days):
    return dt + timedelta(days=days)

def reconvert_date(dt):
    return datetime.timestamp(dt)
    

def is_delivery_day(date)->bool:
    day = date.split("/")[0]
    div = specification["day_frequence"]

    return day % div == 0

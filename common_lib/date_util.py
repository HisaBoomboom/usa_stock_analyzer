from datetime import datetime
from datetime import timedelta


def datetime_before_num_days(dt, days):
    return dt - timedelta(days=days)

def datetime_after_num_days(dt, days):
    return dt + timedelta(days=days)


def one_year_after(dt):
    return datetime(dt.year+1, dt.month, dt.day)


def datestr_to_datetime_obj(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")
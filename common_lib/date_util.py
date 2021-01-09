from datetime import datetime
from datetime import timedelta

import pandas as pd


def datetime_before_num_days(dt, days):
    return dt - timedelta(days=days)

def datetime_after_num_days(dt, days):
    return dt + timedelta(days=days)

def one_year_after(dt):
    return datetime(dt.year+1, dt.month, dt.day)


def get_last_updated_date(symbol, config):
    file_path = config.stock_price_file_path(symbol)

    try:
        with open(file_path, 'r') as f:
            df = pd.read_csv(file_path)
    except:
        return None

    last_date_str = df['Date'].tail(n=1).values[0]
    return date_str_to_datetime_obj(last_date_str)


def date_str_to_datetime_obj(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")
import time
from datetime import datetime

import numpy as np
from tqdm import tqdm

from common_lib import *

DEFAULT_INTERVAL = 15
END_DATE = datetime.now()

def main():
    config = config_loader.Config()

    source_symbols = data_loader.load_ticker_symbols_as_list(config)
    split_symbols = np.array_split(source_symbols, 100)

    for symbols in tqdm(split_symbols):
        last_update_list = [date_util.get_last_updated_date(symbol, config) for symbol in symbols]

        # Define most old updated date in set of given symbols files.
        last_updated_date = last_update_list[0]
        for date in last_update_list:
            if last_updated_date > date:
                last_updated_date = date
        start_date = date_util.datetime_after_num_days(last_updated_date, 1)

        if start_date.year == END_DATE.year and start_date.month == END_DATE.month and start_date.day == END_DATE.day:
            print("no update")
        else:
            print("Start date is {}".format(start_date))
            data_downloader.bulk_download_and_fetch_price_data(symbols, start_date, END_DATE, config)
            sleep()


def sleep():
    for _ in tqdm(range(DEFAULT_INTERVAL)):
        time.sleep(1)


if __name__ == "__main__":
    main()
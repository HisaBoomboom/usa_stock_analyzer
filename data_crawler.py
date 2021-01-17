import time
from datetime import datetime

import numpy as np
from tqdm import tqdm

from common_lib import *


START_DATE = datetime(2018, 1, 1)   # Change here if you want to get old/new data.
END_DATE = datetime.now()
DEFAULT_INTERVAL = 60

config = config_loader.Config()
symbols = data_loader.load_ticker_symbols_as_list(config)

def main():
    config = config_loader.Config()
    source_symbols = data_loader.load_ticker_symbols_as_list(config)

    success_list = []
    split_symbols = np.array_split(source_symbols, 100)

    try:
        for symbols in tqdm(split_symbols):
            print("Download symbols...")
            print(symbols)
            data_downloader.bulk_download_stock_price_data(symbols, START_DATE, END_DATE, config)
            success_list += list(symbols)
            sleep()

    except Exception:
        print("Failed to download all data {}/{}".format(len(success_list), len(source_symbols)))
        with open('output/error.log', 'a+') as f:
            f.write("Failed to download all data ({}/{})".format(len(success_list), len(source_symbols)))
            for symbol in success_list:
                f.write(str(symbol))


def sleep():
    print("sleeping... {}".format(DEFAULT_INTERVAL))
    for _ in tqdm(range(DEFAULT_INTERVAL)):
        time.sleep(1)


if __name__ == "__main__":
    main()
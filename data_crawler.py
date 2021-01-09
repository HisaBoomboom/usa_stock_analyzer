import time
from datetime import datetime

import numpy as np

from common_lib import *

START_DATE = datetime(2016, 1, 1)
END_DATE = datetime.now()
DEFAULT_INTERVAL = 60


def main():
    config = config_loader.Config()
    symbols_df = data_loader.load_nasdaq_symbols(config)

    split_symbols = [list(i) for i in np.array_split(symbols_df.Symbol, 100)]
    print(split_symbols)

    for symbols in split_symbols:
        data_downloader.bulk_fetch_nasdaq_stock_data(symbols, START_DATE, END_DATE, config)
        time.sleep(DEFAULT_INTERVAL)

    return


if __name__ == "__main__":
    main()
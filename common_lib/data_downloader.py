from pathlib import Path

import pandas_datareader.data as web
from pandas_datareader.data import get_nasdaq_symbols
import pandas as pd

DATA_SOURCE_KEY = "yahoo"
STOCK_DATA_KEY_LIST = ['High', 'Low', 'Open', 'Close', 'Adj Close', 'Volume']


def fetch_nasdaq_symbols_data(config):
    """
    Download symbols data to local resource directory.
    """
    path = config.nasdaq_symbols_file_path()

    with open(str(path), "w") as f:
        df = get_nasdaq_symbols()
        df.to_csv(f)
        print("success to download data to {}".format(path))


def bulk_fetch_nasdaq_stock_data(symbols, start, end, config):
    """
    Get all stock data of given symbol list, and save data corresponding to each key as csv.
    symbols: list
    """
    all_df = web.DataReader(symbols, DATA_SOURCE_KEY, start=start, end=end)

    for symbol in symbols:
        symbol_keys = [(k, symbol) for k in STOCK_DATA_KEY_LIST]

        # Extract data of key from MultiIndex DataFrame
        df = pd.DataFrame({new_key:all_df[key] for (new_key, key) in zip(STOCK_DATA_KEY_LIST, symbol_keys)})

        file_path = config.nasdaq_stock_price_file_path(symbol)
        with open(file_path, "+w") as f:
            df.to_csv(f)
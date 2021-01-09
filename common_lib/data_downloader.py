import pandas as pd
import pandas_datareader.data as web

DATA_SOURCE_KEY = "yahoo"
STOCK_DATA_KEY_LIST = ['High', 'Low', 'Open', 'Close', 'Adj Close', 'Volume']


def download_stock_price_data(symbol, start, end, config):
    df = web.DataReader(symbol, DATA_SOURCE_KEY, start=start, end=end)

    file_path = config.stock_price_file_path(symbol)
    with open(file_path, "+w") as f:
        df.to_csv(f)

    return df


def bulk_download_stock_price_data(symbols, start, end, config):
    """
    Get all stock data of given symbol list, and save data corresponding to each key as csv.
    symbols: list
    """
    print("start downloading data...")
    all_df = web.DataReader(symbols, DATA_SOURCE_KEY, start=start, end=end)
    print("success to download")

    for symbol in symbols:
        symbol_keys = [(k, symbol) for k in STOCK_DATA_KEY_LIST]

        # Extract data of key from MultiIndex DataFrame
        df = pd.DataFrame({new_key:all_df[key] for (new_key, key) in zip(STOCK_DATA_KEY_LIST, symbol_keys)})

        file_path = config.stock_price_file_path(symbol)
        with open(file_path, "+w") as f:
            df.to_csv(f)


def bulk_download_and_fetch_price_data(symbols, start, end, config):
    """
    Get all data of given symbol list, merge downloaded data with existing data and overwrite.
    """
    print("start downloading data...")
    all_df = web.DataReader(symbols, DATA_SOURCE_KEY, start=start, end=end)
    print("success to download")

    for symbol in symbols:
        print("---- start fetching symbol={} ----".format(symbol))
        symbol_keys = [(k, symbol) for k in STOCK_DATA_KEY_LIST]

        # Extract data of key from MultiIndex DataFrame
        df = pd.DataFrame({new_key: all_df[key] for (new_key, key) in zip(STOCK_DATA_KEY_LIST, symbol_keys)})

        file_path = config.stock_price_file_path(symbol)
        existing_df = pd.read_csv(file_path)

        new_df = pd.concat([existing_df, df])
        new_df.drop_duplicates()

        with open(file_path, 'w') as f:
            new_df.to_csv(f)
        print("---- success ----")
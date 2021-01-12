import pandas as pd

def load_ticker_symbols_as_list(config):
    path = config.ticker_symbols_file_path()

    with open(path, 'r', encoding='utf-8-sig') as f:
        return f.read().splitlines()


def load_stock_data(symbol, config):
    path = config.stock_price_file_path(symbol)
    return pd.read_csv(path, index_col=0, parse_dates=True)
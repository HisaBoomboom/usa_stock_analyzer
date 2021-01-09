import pandas as pd

TICKER_SYMBOL_FILE_CODE_KEY = "現地コード"

def load_ticker_symbols_as_list(config):
    path = config.ticker_symbols_file_path()
    df = pd.read_csv(path, sep=',')

    return list(df[TICKER_SYMBOL_FILE_CODE_KEY])

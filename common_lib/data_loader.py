import pandas as pd
from pathlib import Path

def load_nasdaq_symbols(config):
    path = config.nasdaq_symbols_file_path()
    return pd.read_csv(path, sep=',')
import os
import re
from pathlib import Path


def is_target_symbol_stock_data_exists(symbol, config):
    file_path = config.nasdaq_stock_price_file_path(symbol)
    return os.path.exists(file_path)

def load_ticker_symbols_as_list(config):
    path = config.ticker_symbols_file_path()

    with open(path, 'r') as f:
        return f.read().splitlines()

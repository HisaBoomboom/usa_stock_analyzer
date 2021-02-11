import pandas as pd
from tqdm import tqdm

from analyzer_lib import *
from common_lib import *


def main():
    config = config_loader.Config()
    symbols = data_loader.load_ticker_symbols_as_list(config)

    sell_recommend = []
    buy_recommend = []
    for symbol in tqdm(symbols):
        flag = recommend(symbol, 1, config)
        if flag == 1:
            buy_recommend.append(symbol)
        elif flag == 2:
            sell_recommend.append(symbol)

    with open('output/summary-buy.txt', 'w+') as f:
        print("==== BUY TIMING ====")
        for symbol in buy_recommend:
            print(symbol)
            f.write(symbol + '\n')

    with open('output/summary-sell.txt', 'w+') as f:
        print("==== SELL TIMING ====")
        for symbol in sell_recommend:
            print(symbol)
            f.write(symbol + '\n')


def recommend(symbol, days, config):
    """
    Scan symbol stock data and return True if it's buy timing.
    """
    all_data = data_loader.load_stock_data(symbol, config)
    prices_df = all_data['Close']
    prices_df = prices_df['2020':]

    df = pd.DataFrame({
        'Price': prices_df,
        'SMA25': technical_analyze_tool.calc_sma(prices_df, 25),
        'SMA75': technical_analyze_tool.calc_sma(prices_df, 75),
        'SMA120': technical_analyze_tool.calc_sma(prices_df, 120),
        'MACD2': technical_analyze_tool.calc_macd2(prices_df),
        'RSI14': technical_analyze_tool.calc_rsi(prices_df, 14)
    })
    prices = df['Price'].values

    buy_hist = []
    sell_hist = []
    for i in range(days):
        if trade_analyzer.is_buy_timing(len(prices) - i - 1, df):
            ix = len(prices) - i - 1
            buy_hist.append((ix, prices[ix]))

        if trade_analyzer.is_sell_timing(len(prices) - i - 1, df):
            ix = len(prices) - i - 1
            sell_hist.append((ix, prices[ix]))

    if len(buy_hist) != 0 or len(sell_hist) != 0:
        if trade_analyzer.is_buy_timing(len(prices) - 1, df):
            return 1

        if trade_analyzer.is_sell_timing(len(prices) - 1, df):
            return 2

    return 0


if __name__ == "__main__":
    main()
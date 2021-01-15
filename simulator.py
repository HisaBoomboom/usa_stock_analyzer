import pandas as pd

from analyzer_lib import *
from common_lib import *

import numpy as np
from tqdm import tqdm


def main():
    config = config_loader.Config()
    symbols = data_loader.load_ticker_symbols_as_list(config)

    sell_recommend = []
    buy_recommend = []
    for symbol in tqdm(symbols):
        flag = recommend(symbol, 3, config)
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


def simulate(symbol, config):
    """
    Walk through stock price data, mark buy/sell timings, and output result if you buy/sell stocks at those timings.
    """
    all_data = data_loader.load_stock_data(symbol, config)
    prices_df = all_data['Close']
    prices_df = prices_df['2020':]

    macd = technical_analyze_tool.calc_macd(prices_df)
    sig = technical_analyze_tool.calc_macd_signal(prices_df)

    df = pd.DataFrame({
        'Price': prices_df,
        'SMA25': technical_analyze_tool.calc_sma(prices_df, 25),
        'SMA75': technical_analyze_tool.calc_sma(prices_df, 75),
        'SMA120': technical_analyze_tool.calc_sma(prices_df, 120),
        'MACD2': macd - sig
    })
    prices = df['Price'].values

    benefit_hist = []
    buy_flag = True
    buy_ind = None

    for i in range(len(prices)):
        if prices[i] == None:
            continue

        # Buy timing
        if buy_flag and trade_analyzer.is_buy_timing(i, df):
            buy_ind = i
            buy_flag = False
            continue

        # Sell timing
        if buy_flag == False and trade_analyzer.is_sell_timing(i, df):
            benefit_ratio = prices[buy_ind] / prices[i]
            benefit_hist.append(benefit_ratio)
            buy_flag = True

    benefit_hist = [i for i in benefit_hist if not np.isnan(i)]
    return benefit_hist


def recommend(symbol, days, config):
    all_data = data_loader.load_stock_data(symbol, config)
    prices_df = all_data['Close']
    prices_df = prices_df['2020':]

    macd = technical_analyze_tool.calc_macd(prices_df)
    sig = technical_analyze_tool.calc_macd_signal(prices_df)

    df = pd.DataFrame({
        'Price': prices_df,
        'SMA25': technical_analyze_tool.calc_sma(prices_df, 25),
        'SMA75': technical_analyze_tool.calc_sma(prices_df, 75),
        'SMA120': technical_analyze_tool.calc_sma(prices_df, 120),
        'MACD2': macd - sig
    })
    prices = df['Price'].values

    buy_hist = []
    sell_hist = []
    for i in range(days):
        if trade_analyzer.is_buy_timing(len(prices)-i-1, df):
            ix = len(prices)-i-1
            buy_hist.append((ix, prices[ix]))

        if trade_analyzer.is_sell_timing(len(prices)-i-1, df):
            ix = len(prices) - i - 1
            sell_hist.append((ix, prices[ix]))

    if len(buy_hist) != 0 or len(sell_hist) != 0:
        graph.save_trade_hist(df, buy_hist, sell_hist, symbol)

        if trade_analyzer.is_buy_timing(len(prices)-1, df):
            return 1

        if trade_analyzer.is_sell_timing(len(prices)-1, df):
            return 2
        
    return 0


if __name__ == "__main__":
    main()
import plotly.graph_objects as go

import mplfinance as mpf
import matplotlib as mpl
import matplotlib.pyplot as plt

from common_lib import *
import pandas as pd
from analyzer_lib import *


def main():
    config = config_loader.Config()
    symbols = data_loader.load_ticker_symbols_as_list(config)

    result = []
    for symbol in symbols:
        (benefit, ratio) = analyze(symbol, config)
        result.append("{} {} {}".format(symbol, benefit, ratio))
        break

    print("#################")
    print("SUMMARY")
    with open("output/summary.txt", 'w+') as f:
        for i in result:
            f.write(i)


def analyze(symbol, config):
    all_data = data_loader.load_stock_data(symbol, config)
    all_data.set_index('Date', inplace=True)

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

    trading_hist = []
    buy = None
    for i in range(len(prices)):
        if prices[i] == None:
            continue

        if buy == None and trade_analyzer.is_buy_timing(i, df):
            buy = (i, prices[i])
            continue

        if buy != None and trade_analyzer.is_sell_timing(i, df):
            trading_hist.append([buy, (i, prices[i])])
            buy = None

    total_benefit_ratio = 1
    win_count = 0
    lose_count = 0
    for trade in trading_hist:
        buy_price = trade[0][1]
        sell_price = trade[1][1]

        benefit_ratio = (sell_price / buy_price)
        total_benefit_ratio *= benefit_ratio
        win_count += 1 if benefit_ratio > 0 else 0
        lose_count += 1 if benefit_ratio < 0 else 0


    print("###### RESULT #######")
    print("SYMBOL = {}".format(symbol))
    print("TOTAL BENEFIT = {}".format(total_benefit_ratio))
    print("TRADE COUNT = {}".format(len(trading_hist)))

    win_ratio = win_count/(win_count + lose_count) if not (win_count + lose_count)==0 else None
    print("Win Ratio = {}".format(win_ratio))

    graph.plot_trade_hist(df, trading_hist, symbol)

    return ((total_benefit_ratio, win_ratio))


if __name__ == "__main__":
    main()
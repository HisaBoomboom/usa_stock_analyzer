import pandas as pd

from analyzer_lib import *
from common_lib import *

import numpy as np

def main():
    config = config_loader.Config()
    symbols = data_loader.load_ticker_symbols_as_list(config)

    total_benefit_hist = []
    for symbol in symbols:
        trading_hist = simulate(symbol, config)
        print("===== {} =====".format(symbol))
        print(trading_hist)
        if len(trading_hist) != 0:
            total_benefit_hist += trading_hist

    print("#################")
    print("SUMMARY")
    with open("output/summary.txt", 'w+') as f:
        for i in total_benefit_hist:
            f.write(str(i) + '\n')

        all_prod = np.prod(total_benefit_hist)
        f.write("RESULT\n")
        f.write(str(all_prod))
        print("Total Benefit Ratio {}".format(all_prod))


def simulate(symbol, config):
    """
    Walk through stock price data, mark buy/sell timings, and output result if you buy/sell stocks at those timings.
    """
    all_data = data_loader.load_stock_data(symbol, config)
    prices_df = all_data['Close']
    # prices_df = prices_df['2019':]

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

    trading_hist = []       # Each element should be [(i, buy-price), (i, sell-price)]
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
            trading_hist.append([(buy_ind, prices[buy_ind]), (i, prices[i])])
            buy_flag = True

    benefit_hist = [i for i in benefit_hist if not np.isnan(i)]
    total_benefit_ratio = np.prod(benefit_hist)

    if len(benefit_hist) != 0:
        graph.save_trade_hist(df, trading_hist, symbol)

    return benefit_hist


if __name__ == "__main__":
    main()
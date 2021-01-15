import pandas as pd

from analyzer_lib import *
from common_lib import *

import numpy as np
from tqdm import tqdm


RESULT_FILE_NAME = 'output/simulate_benefit.txt'
RESULT_HISTOGRAM_NAME = 'output/simulate_benefit.png'

WIN_PLOT_THRESHOLD = 1.2    # Plot as graph if result of benefit ratio is over than this threshold
LOSE_PLOT_THRESHOLD = 0.8


def main():
    config = config_loader.Config()
    symbols = data_loader.load_ticker_symbols_as_list(config)

    total_benefit_hist = []
    for symbol in tqdm(symbols):
        benefit_hist = simulate(symbol, config)
        if len(benefit_hist) != 0:
            total_benefit_hist += benefit_hist

    with open(RESULT_FILE_NAME, 'w+') as f:
        for benefit in total_benefit_hist:
            f.write(str(benefit) + '\n')

    graph.save_histogram(total_benefit_hist, RESULT_HISTOGRAM_NAME)


def simulate(symbol, config):
    """
    Walk through stock price data, mark buy/sell timings, and output result if you buy/sell stocks at those timings.
    """
    all_data = data_loader.load_stock_data(symbol, config)
    prices_df = all_data['Close']

    df = pd.DataFrame({
        'Price': prices_df,
        'SMA25': technical_analyze_tool.calc_sma(prices_df, 25),
        'SMA75': technical_analyze_tool.calc_sma(prices_df, 75),
        'SMA120': technical_analyze_tool.calc_sma(prices_df, 120),
        'MACD2': technical_analyze_tool.calc_macd2(prices_df)
    })
    prices = df['Price'].values

    benefit_hist = []
    buy_hist = []
    sell_hist = []

    buy_flag = True
    buy_ind = None

    for i in range(len(prices)):
        if prices[i] == None:
            continue

        # Buy timing
        if buy_flag and trade_analyzer.is_buy_timing(i, df):
            buy_ind = i
            buy_hist.append((i, prices[i]))
            buy_flag = False
            continue

        # Sell timing
        if buy_flag == False and trade_analyzer.is_sell_timing(i, df):
            benefit_ratio = prices[buy_ind] / prices[i]
            sell_hist.append((i,prices[i]))
            benefit_hist.append(benefit_ratio)
            buy_flag = True

    benefit_hist = [i for i in benefit_hist if not np.isnan(i)]

    for benefit in benefit_hist:
        if benefit > WIN_PLOT_THRESHOLD or benefit < LOSE_PLOT_THRESHOLD:
            graph.save_trade_hist(df, buy_hist, sell_hist, symbol)
            return benefit_hist

    return benefit_hist


if __name__ == "__main__":
    main()
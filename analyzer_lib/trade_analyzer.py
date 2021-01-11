from . import technical_analyze_tool
import numpy as np

def is_buy_timing(i, df):
    if i == 0:
        return False

    prices = df['Price'].values
    sma25 = df['SMA25'].values
    sma75 = df['SMA75'].values
    sma120 = df['SMA120'].values
    macd2 = df['MACD2'].values

    prices_prev = prices[i-5:i]
    sma25_prev = sma25[i-5:i]
    sma75_prev = sma75[i-5:i]
    sma120_prev = sma120[i-5:i]
    macd2_prev = macd2[i-5:i]

    if contains_nan(prices_prev + sma25_prev + sma75_prev + sma120_prev + macd2_prev):
        return False

    # Check golden cross
    if not technical_analyze_tool.is_golden_cross(macd2[i-1], macd2[i]):
        return False

    # Stock price is getting growth
    if not technical_analyze_tool.is_all_prices_are_higher_than_trend(prices[i-5:i], sma75[i-5:i]):
        return False

    # Slope is plus
    if None in sma25[i-5:i] + sma75[i-5:i] + sma120[i-5:i]:
        return False

    if technical_analyze_tool.calc_regression_line_slope(sma25[i-5:i]) < 0:
        return False

    if technical_analyze_tool.calc_regression_line_slope(sma75[i-5:i]) < 0:
        return False

    if technical_analyze_tool.calc_regression_line_slope(sma120[i-5:i]) < 0:
        return False

    return True


def is_sell_timing(i, df):
    if i == 0:
        return False

    prices = df['Price'].values
    sma25 = df['SMA25'].values
    sma75 = df['SMA75'].values
    sma120 = df['SMA120'].values
    macd2 = df['MACD2'].values

    if prices[i] < sma25[i]:
        return True

    if prices[i] < sma75[i]:
        return True

    if technical_analyze_tool.is_dead_cross(macd2[i-1], macd2[i]):
        return True

    if technical_analyze_tool.calc_regression_line_slope(sma75[i-5:i]) < 0:
        return True

    if technical_analyze_tool.calc_regression_line_slope(sma120[i-5:i]) < 0:
        return True
    return False


def contains_nan(data):
    for i in data:
        if np.isnan(i):
            return True
    return False
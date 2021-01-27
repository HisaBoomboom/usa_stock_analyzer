from . import technical_analyze_tool
import numpy as np

def is_buy_timing(i, df):
    """
    i: index of df
    df: DataFrame type data contains all stock data with date index
    """
    if i <= 25:
        return False

    prices = df['Price'].values
    sma25 = df['SMA25'].values
    macd2 = df['MACD2'].values

    prices_prev = prices[i-5:i]
    sma25_prev = sma25[i-5:i]
    macd2_prev = macd2[i-5:i]

    if has_nan(prices_prev) or has_nan(sma25_prev) or has_nan(macd2_prev):
        return False

    # Multiple cross can be noise.
    if not technical_analyze_tool.has_single_cross(macd2_prev):
        return False

    # Golden cross is occurred at yesterday
    if not technical_analyze_tool.is_golden_cross(macd2[i-2], macd2[i-1]):
        return False

    # Today not getting bad
    if not (prices[i-1] <= prices[i]):
        return False
    
    if technical_analyze_tool.calc_regression_line_slope(sma25_prev) < 0:
        return False

    return True


def is_sell_timing(i, df):
    """
    i: index of df
    df: DataFrame type data contains all stock data with date index
    """
    if i == 0:
        return False

    prices = df['Price'].values
    sma25 = df['SMA25'].values
    sma75 = df['SMA75'].values
    sma120 = df['SMA120'].values
    macd2 = df['MACD2'].values

    prices_prev = prices[i - 5:i]
    sma25_prev = sma25[i - 5:i]
    sma75_prev = sma75[i - 7:i]
    sma120_prev = sma120[i - 15:i]
    macd2_prev = macd2[i - 5:i]

    if has_nan(prices_prev) or has_nan(sma25_prev) or has_nan(sma75_prev) or has_nan(sma120_prev) or has_nan(macd2_prev):
        return False

    if prices[i] < sma75[i] or prices[i] < sma120[i]:
        return True

    if technical_analyze_tool.has_single_cross(macd2_prev) and technical_analyze_tool.is_dead_cross(macd2[i-1], macd2[i]):
        return True

    return False


def has_nan(data):
    for i in data:
        if np.isnan(i):
            return True
    return False
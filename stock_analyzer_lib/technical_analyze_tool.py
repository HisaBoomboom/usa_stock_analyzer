import pandas as pd

def calc_sma(df, days):
    return df.rolling(window=days).mean()


def calc_macd(df):
    ema12 = calc_ema(df, 12)
    ema26 = calc_ema(df, 26)
    return ema12 - ema26


def calc_macd_signal(df):
    macd = calc_macd(df)
    return calc_sma(macd, 9)


def calc_ema(df, span):
    return df.ewm(span=span, adjust=False).mean()


def calc_regression_line_slope(data):
    """
    Calculate slope(a) of regression line calculated by given data.
    """
    if None in data:
        return None

    x_list = list(range(len(data)))
    y_list = data

    n = len(x_list)
    x_ave = sum(x_list) / n
    y_ave = sum(y_list) / n

    x_dispersion = sum([(xi - x_ave) ** 2 for xi in x_list]) / n
    covariance = sum([(xi - x_ave) * (yi - y_ave) for xi, yi in zip(x_list, y_list)]) / n

    return covariance / x_dispersion


def is_all_prices_are_higher_than_trend(prices, trend):
    """
    Return true if all price is over the trend line.
    """
    if None in prices or None in trend:
        return False

    diff = [prices[i] - trend[i] for i in range(len(prices))]

    for d in diff:
        if d < 0:
            return False
    return True


def is_buy_timing(i, df):
    if i == 0:
        return False

    prices = df['Price'].values
    sma25 = df['SMA25'].values
    sma75 = df['SMA75'].values
    sma120 = df['SMA120'].values
    macd2 = df['MACD2'].values

    # Check golden cross
    if not is_golden_cross(macd2[i-1], macd2[i]):
        return False

    if not is_all_prices_are_higher_than_trend(prices[i-5:i], sma75[i-5:i]):
        return False

    if calc_regression_line_slope(sma25[i-5:i]) < 0:
        return False

    if calc_regression_line_slope(sma75[i-5:i]) < 0:
        return False

    if calc_regression_line_slope(sma120[i-5:i]) < 0:
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

    if is_dead_cross(macd2[i-1], macd2[i]):
        return True

    if calc_regression_line_slope(sma75[i-5:i]) < 0:
        return True

    if calc_regression_line_slope(sma120[i-5:i]) < 0:
        return True

    return


def is_golden_cross(v1, v2):
    if None in [v1, v2]:
        return False
    return v1<0 and v2>0

def is_dead_cross(v1, v2):
    if None in [v1, v2]:
        return False
    return v1>0 and v2<0
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


import matplotlib.pyplot as plt

def plot_trade_hist(df, trading_hist):
    prices = df['Price'].values
    sma25 = df['SMA25'].values
    sma75 = df['SMA75'].values
    sma120 = df['SMA120'].values
    macd2 = df['MACD2'].values

    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)

    ax1.plot(prices)
    ax1.plot(sma25)
    ax1.plot(sma75)
    ax1.plot(sma120)

    ax2.plot(macd2)
    ax2.axhline([0], xmin=0, xmax=1)
    ax1.set_xlim([0, len(prices)])
    ax2.set_xlim([0, len(prices)])

    for trade in trading_hist:
        buy = trade[0]
        sell = trade[1]
        ax1.plot(buy[0], buy[1], marker="^", markersize=10, color='b')
        ax1.plot(sell[0], sell[1], marker="v", markersize=10, color='r')
        ax1.axvline(buy[0], ymin=0, ymax=1, color='b', linestyle='dotted')
        ax1.axvline(sell[0], ymin=0, ymax=1, color='r', linestyle='dotted')
        ax2.axvline(buy[0], ymin=0, ymax=1, color='b', linestyle='dotted')
        ax2.axvline(sell[0], ymin=0, ymax=1, color='r', linestyle='dotted')
    plt.show()


def get_golden_cross_points(prices, macd2):
    result = []
    for i in range(len(prices)):
        if i == 0 or prices[i] == None or macd2[i] == None:
            continue

        if is_golden_cross(macd2[i-1], macd2[i]):
            result.append((i, prices[i]))

    return result


def is_golden_cross(v1, v2):
    if v1 < 0 and v2 > 0:
        return True
    else:
        return False


def get_dead_cross_points(prices, macd2):
    result = []
    for i in range(len(prices)):
        if i == 0 or prices[i] == None or macd2[i] == None:
            continue

        if is_dead_cross(macd2[i - 1], macd2[i]):
            result.append((i, prices[i]))

    return result


def is_dead_cross(v1, v2):
    if v1>0 and v2<0:
        return True
    else:
        return False
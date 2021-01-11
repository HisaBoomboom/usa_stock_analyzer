import matplotlib.pyplot as plt


def plot_trade_hist(df, trading_hist, symbol):
    plot_or_save_trade_hist(df, trading_hist, symbol, 'plot')


def save_trade_hist(df, trading_hist, symbol):
    plot_or_save_trade_hist(df, trading_hist, symbol, 'save')


def plot_or_save_trade_hist(df, trading_hist, symbol, flag):
    plt.clf()

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

    ax1.set_xlim([120, len(prices)])
    ax2.set_xlim([120, len(prices)])

    for trade in trading_hist:
        buy = trade[0]
        sell = trade[1]
        ax1.plot(buy[0], buy[1], marker="^", markersize=10, color='b')
        ax1.plot(sell[0], sell[1], marker="v", markersize=10, color='r')
        ax1.axvline(buy[0], ymin=0, ymax=1, color='b', linestyle='dotted')
        ax1.axvline(sell[0], ymin=0, ymax=1, color='r', linestyle='dotted')
        ax2.axvline(buy[0], ymin=0, ymax=1, color='b', linestyle='dotted')
        ax2.axvline(sell[0], ymin=0, ymax=1, color='r', linestyle='dotted')

    if flag == 'plot':
        plt.show()
    elif flag == 'save':
        plt.savefig("output/{}.png".format(symbol))
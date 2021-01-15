import matplotlib.pyplot as plt


def plot_trade_hist(df, buy_hist, sell_hist, file_name):
    plot_or_save_trade_hist(df, buy_hist, sell_hist, file_name, 'plot')


def save_trade_hist(df, buy_hist, sell_hist, file_name):
    plot_or_save_trade_hist(df, buy_hist, sell_hist, file_name, 'save')


def plot_or_save_trade_hist(df, buy_hist, sell_hist, file_name, flag):
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

    for trade in buy_hist:
        ix = trade[0]
        price = trade[1]
        ax1.plot(ix, price, marker="^", markersize=10, color='b')
        ax1.axvline(ix, ymin=0, ymax=1, color='b', linestyle='dotted')
        ax2.axvline(ix, ymin=0, ymax=1, color='b', linestyle='dotted')

    for trade in sell_hist:
        ix = trade[0]
        price = trade[1]
        ax1.plot(ix, price, marker="v", markersize=10, color='r')
        ax1.axvline(ix, ymin=0, ymax=1, color='r', linestyle='dotted')
        ax2.axvline(ix, ymin=0, ymax=1, color='r', linestyle='dotted')

    if flag == 'plot':
        plt.show()
    elif flag == 'save':
        plt.savefig("output/{}.png".format(file_name))

    plt.clf()
    plt.close()


def plot_benefit_summary_histogram(data, file_name):
    plt.clf()
    plt.hist(data)
    plt.savefig(file_name)
    plt.close()
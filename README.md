# usa_stock_analyzer
![](https://img.shields.io/badge/Python-3.6.2-green.svg?style=flat-square&logo=python)

Tool for checking buy/sell timing based on stock price data.

# Preparation
## Download stock price data
### 1. Setup local resource directory
Specify the target directory path as an environment variable `${RESOURCE_BASE_DIR}`, and then, create directory whose name is `stock_price` under it. Downloaded data is placed under this directory.
```shell
export RESOURCE_BASE_DIR=/path/to/local/resource/
mkdir ${RESOURCE_BASE_DIR}/stock_price
```

### 2. Preparation
Create `symbols.txt` under local resource directory which contains list of target ticker symbols. **This should be done manually.**

The stock data in this file are going to be downloaded by application.
```shell
head ${RESOURCE_BASE_DIR}/symbols.txt
A
AA
AAL
AAN
AAOI
AAON
AAP
AAPL
AAWW
AAXN
```

### 3. Run `data_crawler.py`
Target stock data is downloaded by **pandas-datareader**.
In default, application tries to get data from `2018-01-01` to now, and save it as **csv file**.
```shell
python data_crawler.py
```

File name format is like this `{symbol}_stock_price.csv`
```shell
head ${RESOURCE_BASE_DIR}/stock_price/A_stock_price.csv
Date,High,Low,Open,Close,Adj Close,Volume
2018-01-02,67.88999938964844,67.33999633789061,67.41999816894531,67.59999847412111,65.87785339355469,1047800.0
2018-01-03,69.48999786376953,67.59999847412111,67.62000274658203,69.31999969482422,67.55403900146484,1698900.0
2018-01-04,69.81999969482422,68.77999877929689,69.54000091552734,68.80000305175781,67.04727935791016,2230700.0
2018-01-05,70.09999847412111,68.73000335693361,68.73000335693361,69.90000152587889,68.11924743652344,1632500.0
2018-01-08,70.33000183105469,69.55000305175781,69.73000335693361,70.05000305175781,68.26544189453125,1613400.0
2018-01-09,72.33000183105469,70.16999816894531,70.68000030517578,71.7699966430664,69.94162750244139,2666100.0
2018-01-10,71.44999694824219,70.11000061035156,71.44999694824219,70.79000091552734,68.98657989501953,2957200.0
2018-01-11,71.18000030517578,70.30000305175781,70.91999816894531,70.80000305175781,68.99632263183594,1511100.0
2018-01-12,71.86000061035156,70.5,70.7300033569336,71.7300033569336,69.90264129638672,1448100.0
```

## Refresh local data
If you already have stock prices data downloaded by `data_crawler.py` and you want to refresh data as current time.
You can use `data_fetcher.py` to retrieve lack data.
```shell
python data_fetcher.py
```


# Analyze stock data
`analyzer_lib.trade_analyzer.py` is the implementation of analyzing tool to determine buy/sell timing. 
`analyzer_lib.trade_analyzer.is_buy_timing` returns `True` if i-th day of given data (df) is the buy timing. `analyzer_lib.trade_analyzer.is_sell_timing` is the opposite method, and it considers sell timing.

You can edit these two methods to customize your original algorithm to analyze stock data.

## Simulate stock trade
Once you create new algorithms, you can check the performance of it by using **simulator**. `simulator.py` scans all the stock price data in local resource directory, applies buy/sell algorithm and check if stock price become higher than buy date.
```shell
python simulator.py 
```

A result is outputted to `output` directory. `simulate_benefit.txt` is the summary file of all trades based on your algorithm.

For example, if your algorithm buys stock `400$` and sell `500$`.
```shell
buy: 400
sell: 500
benefit ratio: 1.25
```
In this case, line `1.25` is added in `simulate_benefit.txt`. A histogram of all the benefit ratios is saved as `simulate_benefit.png`.

Also, in case where a benefit ratio is lower than 0.8 or bigger than 1.2, a graph that shows timings of trade is occurred is saved under `output` so that you can check how your algorithm works (blue marker shows buy timing, and red one shows sell timing).
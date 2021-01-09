# usa_stock_analyzer
![](https://img.shields.io/badge/Python-3.6.2-green.svg?style=flat-square&logo=python)


## Download stock price data
Place symbols.txt which contains ticker-symbol
in each line under local resource directory.
```shell
$cat /path/for/local/resource/symbols.txt
A
AA
AAL
...
```
Download stock data of ticker-symbols described in `symbols.txt` via pandas-datareader.
```shell
export="/path/for/local/resource"
python data_crawler.py
```


## Refresh local data
Download data from last updated date to now.
```shell
export="/path/for/local/resource"
python data_fetcher.py
```
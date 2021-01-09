# usa_stock_analyzer
![](https://img.shields.io/badge/Python-3.6.2-green.svg?style=flat-square&logo=python)


## Download stock price data
Place symbols.txt which contains ticker-symbol
in each line under local resource directory.
```shell
$pwd 
/path/for/local/resource

$ls
symbols.txt
```

Download stock data of ticker-symbols described in `symbols.txt` via pandas-datareader.
```shell
export="LOCAL RESOURCE DIRECTORY"
python data_crawler.py
```

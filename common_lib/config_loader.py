import os
import yaml

from pathlib import Path

class Config:

    def __init__(self):
        self.__local_resource_dir = os.environ.get("RESOURCE_BASE_DIR")
        if self.__local_resource_dir == None:
            print("ERROR: RESOURCE_BASE_DIR is not specified")
            exit(1)

        with open("configs/local_resource.yaml") as f:
            self.__local_resource_config = yaml.safe_load(f)


    @property
    def local_resource_dir(self):
        return self.__local_resource_dir


    def ticker_symbols_file_path(self):
        config = self.__local_resource_config.get("ticker_symbols")
        base = self.__local_resource_dir
        dir = config.get("dir_path")
        file_name = config.get("file_name")
        return str(Path(base, dir, file_name))


    def stock_price_file_path(self, symbol):
        config = self.__local_resource_config.get("stock_price")
        base = self.__local_resource_dir
        dir = config.get("dir_path")
        file_name = config.get("file_name").format(symbol)
        return str(Path(base, dir, file_name))

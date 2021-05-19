from BinanceRowData import *
import requests
import time
from enum import Enum
import json

"""  """
class Interval(str, Enum):
    ONE_MINUTE = '1m'
    ONE_HOUR = '1h'
    ONE_DAY = '1d'
    ONE_WEEK = '1w'
    ONE_MONTH = '1M'

""" Class to retrieve data from Binance. """
class BinanceDataFeed:

    # Base URL for binance API
    BASE_URL = 'https://api.binance.com'

    # API Version
    API_VERSION = 'v3'

    # List of the symbols trader on binance
    symbols = None

    """ Class constructor. """
    def __init__(self):
        self.__set_symbols()
        print()

    """ Retrieve data about specific cryptocurrency pair. """
    def get_price_data(self, symbol, interval = '1d', start_time = None, end_time = None, limit = 1000):
        path = '/api/{0}/klines'.format(BinanceDataFeed.API_VERSION)
        url = BinanceDataFeed.BASE_URL + path

        if not (start_time != None and end_time != None):
            if start_time == None:
                start_time = 1
            if end_time == None:
                end_time = int(time.time()) * 1000

        if start_time > end_time:
            print('Error start time cannot be earlier than end time!')

        data = []
        while True:
            params = {
                'symbol' : symbol,
                'interval' : interval,
                'limit' : limit,
                'startTime' : start_time,
                'endTime' : end_time
            }

            response = requests.get(url = url, params = params)
            blob = response.json()
            data.append(blob)
            curr_last_time = BinanceRowData(blob[len(blob)-1]).raw_close_time
            if curr_last_time > end_time:
                break

            start_time = curr_last_time

        return data

    """ Fetches entire information about all the symbols at Exchange. """
    def get_exchange_info(self):
        path = '/api/{0}/exchangeInfo'.format(BinanceDataFeed.API_VERSION)
        url = BinanceDataFeed.BASE_URL + path
        response = requests.get(url = url)
        return response.json()

    """ Fetches list of the symbols currently traded on Binance. """
    def __set_symbols(self):
        if BinanceDataFeed.symbols is None:
            exchange_info = self.get_exchange_info()
            symbols = []
            for info in exchange_info['symbols']:
                symbol = info['symbol']
                if symbol[-4:] == 'USDT':
                    symbols.append(symbol)
                symbols.sort()
            BinanceDataFeed.symbols = symbols

    """ Print the row data. """
    @staticmethod
    def print_row_data(binance_row_data):
        print('Open time : ' + binance_row_data.open_time + ' , Close price : ' + binance_row_data.close_price)
        # print(binance_row_data.high_price)
        # print(binance_row_data.low_price)
        # print(binance_row_data.close_price)
        # print(binance_row_data.volume)
        # print(binance_row_data.close_time)


if __name__ == '__main__':

    df = BinanceDataFeed()
    data = df.get_price_data(
        symbol = 'MATICUSDT', 
        interval = Interval.ONE_DAY
    )

    for blob in data:
        for row in blob:
            row = BinanceRowData(row)
            BinanceDataFeed.print_row_data(row)
    
    for symbol in BinanceDataFeed.symbols:
        print(symbol)

    # monthly_data = df.get_price_data('BTCUSDT', interval = Interval.ONE_MONTH, limit = 20)
    # start_time = BinanceRowData(monthly_data[0]).raw_open_time
    # print(start_time)
    
    #print(BinanceRowData.convert_epoch_to_datetime(1620498600000))
    
        # start_time = BinanceRowData.convert_datetime_to_epoch('2018-01-01'),
        # end_time = BinanceRowData.convert_datetime_to_epoch('2018-01-02'),
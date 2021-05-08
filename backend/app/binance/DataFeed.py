import requests
import time
from BinanceRowData import *

""" Class to retrieve data from Binance. """
class DataFeed:
    BINANCE_BASE_URL = 'https://api.binance.com'

    def getPriceData(self, symbol, interval = '1d', start_time = None, end_time = None, limit = None):
        path = '/api/v3/klines?'
        url = DataFeed.BINANCE_BASE_URL + path
        params = {'symbol' : symbol, 'interval' : interval}

        if limit != None:
            params['limit'] = limit

        response = requests.get(url = url, params = params)
        return response

if __name__ == '__main__':

    df = DataFeed()
    data = df.getPriceData('BTCUSDT', limit = 1500).json()

    for i in range(len(data)):
        row = BinanceRowData(data[i])
        print(row.close_time)

    print(len(data))
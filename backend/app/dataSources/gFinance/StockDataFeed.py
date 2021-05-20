import os, json
import googleService


""" Class to provide stock data. """

class StockDataFeed:

    # List of the symbols trader on binance
    symbols = None

    # GoogleService
    googleService = None

    """ Constructor. """
    def __init__(self):
        #self.__set_symbols()
        #googleService = GoogleService('','')
        print()
    

    """ Fetches list of the symbols currently traded on NSE. """
    def __set_symbols(self):
        if StockDataFeed.symbols is None:
            StockDataFeed.symbols = self.get_stockdb_index()

    
    def get_daily_stock_data():
        print()


s = StockDataFeed()
print()
from ... googleServices.GoogleService import GoogleService
from ... googleServices.SheetsService import SheetsService
from ... resources import feed



class StockDataFeed:
    """ Class to provide stock data. """

    # List of the symbols trader on binance
    symbol_table = None

    # GoogleService
    googleService = None

    sheetsService = None

    """ Constructor. """
    def __init__(self):
        self.__set_symbols()
        StockDataFeed.googleService = GoogleService()
        StockDataFeed.sheetsService = SheetsService(StockDataFeed.googleService.get_sheets_service())
        self.get_daily_stock_data('ITC')

    """ Fetches list of the symbols currently traded on NSE. """
    def __set_symbols(self):
        if StockDataFeed.symbol_table is None:
            StockDataFeed.symbol_table = feed.get_symbols_info()

    def get_daily_stock_data(self, symbol):
        data = StockDataFeed.sheetsService.read_sheet(StockDataFeed.symbol_table[symbol])
        print(data)
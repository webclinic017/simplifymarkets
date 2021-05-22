from ...googleServices.GoogleService import GoogleService
from ...resources import feed

sheets_service = GoogleService().get_sheets_service()

database_index = feed.get_symbols_info()

class StockDataFeed:
    """ Class to provide stock data. """

    def get_data(self, symbol_list):
        data = {}
        for symbol in symbol_list:
            sheet_id = database_index[symbol]
            stock_data = sheets_service.read_sheet(sheet_id)
            data[symbol] = stock_data
        return data


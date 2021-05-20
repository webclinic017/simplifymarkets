import time, datetime

""" Class to handle the response data from Binance. """
class BinanceRowData:

    """ Class constructor. """
    def __init__(self, row):
        self.raw_open_time = int(row[0])
        self.open_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.raw_open_time/1000.0))
        self.open_price = row[1]
        self.high_price = row[2]
        self.low_price = row[3]
        self.close_price = row[4]
        self.volume = row[5]
        self.raw_close_time = int(row[6])
        self.close_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.raw_close_time/1000.0))
        self.quote_asset_vol = row[7]
        self.trade_count = row[8]
        self.taker_buy_base_vol = row[9]
        self.taker_buy_quote_vol = row[10]

    @staticmethod
    def convert_epoch_to_datetime(epoch_time, ms = True):
        if ms == True:
            epoch_time = epoch_time/1000.0
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))

    @staticmethod
    def convert_datetime_to_epoch(date_time, ms = True):
        seconds = int(time.mktime(datetime.datetime.strptime(date_time, "%Y-%m-%d").timetuple()))
        if ms == True:
            return seconds * 1000
        return seconds

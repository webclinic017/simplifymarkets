from datetime import datetime

import backtrader as bt
from backtrader import cerebro
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .dataSources.gFinance.StockDataFeed import StockDataFeed, database_index
from .models import employee, knowledge
from .serializers import (UserSerializer, employeesSerializer,
                          knowledgeSerializer)
from .utility.File import File
from ta.trend import SMAIndicator
import pandas as pd

stock_data_feed = StockDataFeed()
file = File()
knowledge_db = file.read(file_name = 'knowledge_db', path =  settings.BASE_DIR + '\\app\\resources\\', extension = 'json');
holdings = file.read(path='C:\\Users\\91880\\Downloads', file_name='holdings', extension='csv')

class SMA(APIView):

    def get(self, request):
        start_time = datetime.now()

        data = stock_data_feed.get_data(['ITC'])
        itc = data['ITC']
        
        df = pd.DataFrame(data=itc[1:5], columns=itc[0])
        df.Close = pd.to_numeric(df.Close, downcast="float")
        op = df.Close.rolling(2).mean()
        
        #result = df[4].rolling(50).mean()
        return Response(op)


class highest(APIView):

    def get(self, request):
        start_time = datetime.now()
        
        # print("Calculating High ...", flush=True)
        # table = knowledge.objects.all()
        # result = knowledgeSerializer(table, many = True)
        # return Response(result.data)
        result = {}
        symbols_list = []

        for row in holdings:
            if not (row[0] in knowledge_db):
                symbols_list.append(row[0])

        # print(symbols_list, flush=True)

        data = stock_data_feed.get_data(symbols_list)
        print('Data downloaded...', flush=True)

        for symbol in data:
            try:
                blob = {}
                symbol_data = data[symbol]
                highest_price = -1
                hp_datetime = None
                hp_idx = 0
                for i in range(1,len(symbol_data)):
                    # print(hdfc_data[i], flush=True)
                    if float(symbol_data[i][4]) > float(highest_price):
                        highest_price = symbol_data[i][4]
                        hp_datetime = symbol_data[i][0]
                        hp_idx = i

                highest_price = float(highest_price)
                curr_price = float(symbol_data[len(symbol_data)-1][4])
                perc_change_from_high = round(((curr_price - highest_price) / highest_price) * 100, 2)
                number_of_days = len(symbol_data)-1-hp_idx

                blob['highest_price'] = highest_price
                blob['hp_datetime'] = hp_datetime
                blob['perc_change_from_high'] = perc_change_from_high
                blob['number_of_days'] = number_of_days
                result[symbol] = blob
            except Exception as e:
                print(e)


        finish_time = datetime.now()
        execution_time = (finish_time - start_time).total_seconds() * 1000
        print('Latency :' + str(execution_time) + ' ms', flush=True)
        return Response(knowledge_db)

    """
    def post(self):
        return 
    """


def index(request):
    data = StockDataFeed().get_data(['ITC'])
    for symbol in data:
        print(data[symbol][0], flush=True)
        print(data[symbol][1], flush=True)
        break
    return HttpResponse('Nice')


def calculate_all_symbols_avg():
    """ This function is to check what return you would get if you invest in all the companies. """
    start_time = datetime.now()
    # print('st : ' + str(start_time))
    stock_data_feed = StockDataFeed()

    symbols_list = []
    for symbol in database_index:
        symbols_list.append(symbol)

    new_symbols_list = symbols_list[0:10]

    data = stock_data_feed.get_data(new_symbols_list)

    for i in range(len(new_symbols_list)):
        # print(data[new_symbols_list[i]])
        if 1 == 1:
            x = True

    finish_time = datetime.now()
    execution_time = (finish_time - start_time).total_seconds() * 1000

    print('Latency :' + str(execution_time) + ' ms', flush=True)
    return data[new_symbols_list[0]]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class employeeList(APIView):

    def get(self, request):
        employees1 = employee.objects.all()
        result = employeesSerializer(employees1, many=True)
        return Response(result.data)

    """
    def post(self):
        return 
    """


def call_bt_test():
    cerebro = bt.Cerebro()
    data = bt.feeds.YahooFinanceData(dataname='MSFT',
                                     fromdate=datetime(2011, 1, 1),
                                     todate=datetime(2012, 12, 31))
    data = StockDataFeed().get_data(['ITC'])
    cerebro.adddata(data['ITC'])  # Add the data feed

    cerebro.addstrategy(SmaCross)  # Add the trading strategy
    cerebro.run()  # run it all
    cerebro.plot()  # and plot it with a single command


class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position

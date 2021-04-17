from datetime import datetime
import backtrader as bt
from dynamic_params as *

//memory allocation
STRATEGY = DynamicArray()
# Append new element
STRATEGY.append(SmaCross)
len(STRATEGY)

STOCK_ID = DynamicArray()
# Append new element
STOCK_ID.append("resources\MAHABANK.NS.csv")
len(STOCK_ID)







data = bt.feeds.YahooFinanceData(dataname=STOCK_ID,
                                 fromdate=datetime(2020, 5, 6),
                                 todate=datetime(2021, 3, 23))


cerebro = bt.Cerebro() 
cerebro.addanalyzer(bt.analyzers.Returns)
cerebro.optstrategy(VolumeWeightedAveragePrice, idx=[0, 1])
results = cerebro.run(maxcpus=args.maxcpus, optreturn=args.optreturn)
cerebro.adddata(data)  # Add the data feed
cerebro.addstrategy(STRATEGY,pfast=10,pslow=40)  # Add the trading strategy

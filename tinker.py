import dotenv
import os
from os.path import dirname, join
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import time
import requests
import json


import gather_data
import models.test_run as test_run
import models.trade as trade
import models.exchange_rate as exchange_rate
import models.candlestick as candlestick
import strategies.ichimoku as ichimoku
import strategy_test

dotenv.load_dotenv(join(dirname(__file__), '.env'))

# PULL_RESOLUTION = os.environ.get('PULL_RESOLUTION')

# btceth.scheduleRatePulls(interval=PULL_RESOLUTION)
# time.sleep(1)
# results = []

# for i in data2:
#     results.append(i[4])

# plt.plot(results)
# plt.show()

# Overlap data
# https://poloniex.com/public?command=returnChartData&currencyPair=BTC_ETH&start=1501987800&end=1502107800&period=300
# All data
# url = 'https://poloniex.com/public?command=returnChartData&currencyPair=BTC_ETH&start=1438992000&end=9999999999&period=300'


# new_trade = trade.Trade()
# print new_trade.initialize()
# new_trade.test_run_id = '2'
# new_trade.invested_value = '1000'
# new_trade.returned_value = '1010'
# new_trade.buy_time = '1234'
# new_trade.sell_time = '1235235'
# new_trade.create()


# run = test_run.TestRun()
# run.initialize()

# run.strategy = 'New Run'
# run.from_time = 15
# run.to_time = 34
# run.investment = 1000
# run.roi = 1000.0014
# run.parameters = json.dumps(['test', 'one_two'])

candle = candlestick.Candlestick()
# data = candle.fetchAllBetween('ETH', 'BTC', 1498000000)
# # Rate window
data = candle.fetchAllBetween('ETH', 'BTC', 1501987800, 1502107800)
# # One month
# data = candle.fetchAllBetween('ETH', 'BTC', 1501116800)
# # Six months
# data = candle.fetchAllBetween('ETH', 'BTC', 1487116800)
# # All
# data = candle.fetchAll('ETH', 'BTC')

data['rate'] = data['close']

# print data.describe()

# start = time.time()

# data1 = data[:875]
# data2 = data[876:]

# print  data.tail(1).index[0].value // 10 ** 9

# # Strategies

def runCloud(cloud):

    cloud.setTradeThreshold(10025)
    cloud.setInitialInvestment(1000)
    cloud.setResolution(104)
    cloud.run()
    cloud.report()

cloud = ichimoku.Ichimoku(data)
cloud.setExchangeFee(.11)
runCloud(cloud)
# cloud.executeStrategy(data)

# print 'Elapsed:', time.time() - start

# print data.head(1).index[0]
# print data.tail(1).index[0]

# plt.plot(cloud.getSellValues())
# plt.show()

# # Run tests

def test_cloud(cloud):

    cloud_test = strategy_test.StrategyTest(cloud)
    cloud_test.setRange(10000, 10030)
    cloud_test.setInterval(5)
    cloud_test.testThreshold(resolution = 52)
    cloud_test.report()

# test_cloud(cloud)

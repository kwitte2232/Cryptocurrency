import dotenv
import os
from os.path import dirname, join
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import scipy.stats
import time
import requests


import gather_data
import exchange_rate
import strategies.ichimoku as ichimoku
import strategy_test
import trade
import candlestick



dotenv.load_dotenv(join(dirname(__file__), '.env'))

print 'Success'

# PULL_RESOLUTION = os.environ.get('PULL_RESOLUTION')

# btceth.scheduleRatePulls(interval=PULL_RESOLUTION)
# time.sleep(1)
# results = []

# for i in data2:
#     results.append(i[4])

# plt.plot(results)
# plt.show()

# https://poloniex.com/public?command=returnChartData&currencyPair=BTC_ETH&start=1501987800&end=1502107800&period=300

candle = candlestick.Candlestick()
data = candle.fetchAll('ETH', 'BTC')
data['rate'] = data['high'] + data['low'] / 2


print 'Success'

#print data.describe()

# data1 = data[:875]
# data2 = data[876:]

#cloud = ichimoku.Ichimoku(data)
#cloud.setExchangeFee(.11)

# cloud.executeStrategy(data)

# # Strategies

#def runCloud(cloud):

    # cloud.setTradeThreshold(2200)
    #cloud.setInitialInvestment(1000)
    #cloud.setResolution(52)
    #cloud.run()
    #cloud.report()

#runCloud(cloud)

# # Run tests

#def test_cloud(cloud):

    #cloud_test = strategy_test.StrategyTest(cloud)
    #cloud_test.setRange(1000, 6000)
    #cloud_test.setInterval(100)
    #cloud_test.testThreshold(resolution = 50)
    #cloud_test.report()


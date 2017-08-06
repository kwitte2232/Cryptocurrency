import dotenv
import os
from os.path import dirname, join
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import time


import gather_data
import exchange_rate
import strategies.momentum as momentum
import strategies.spike as spike
import strategy_test
import trade

dotenv.load_dotenv(join(dirname(__file__), '.env'))

# PULL_RESOLUTION = os.environ.get('PULL_RESOLUTION')

# btceth.scheduleRatePulls(interval=PULL_RESOLUTION)
# time.sleep(1)

btceth = gather_data.GatherData('BTC', 'ETH')

data = btceth.retrieveExchangeRates();

data1 = data[0:5350]
data2 = data[5351:len(data)]

spike = spike.Spike(data2)
momentum = momentum.Momentum(data2)
spike.setExchangeFee(.11)
momentum.setExchangeFee(.11)

# # Strategies

spike.setTradeThreshold(2200)
spike.setInitialInvestment(1000)
spike.setResolution(50)
spike.run()
spike.report()

# momentum.setTradeThreshold(3250)
# momentum.setInitialInvestment(1000)
# momentum.setResolution(225)
# momentum.run()
# momentum.report()

# # Run tests

results = []

# momentum_test = strategy_test.StrategyTest(momentum)
# momentum_test.setRange(150, 300)
# momentum_test.setInterval(10)
# momentum_test.testResolution(threshold = 3250)
# momentum_test.report()

# spike_test = strategy_test.StrategyTest(spike)
# spike_test.setRange(3000, 4000)
# spike_test.setInterval(200)
# spike_test.testThreshold(resolution = 50)
# spike_test.report()

if len(results):
    plt.plot(results)
    plt.show()

# dotenv.load_dotenv(join(dirname(__file__), '.env'))

# DATA_RESOLUTION = os.environ.get('DATA_RESOLUTION')

# rates = exchange_rate.ExchangeRate().fetchAll()

# price_data = []

# for rate in rates:
#     price_data.append([int(rate[1]), float(rate[4])])

# plt.plot(price_data)

# 0.0817
# 0.08067064
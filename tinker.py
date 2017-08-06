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

# results = []

# for i in data2:
#     results.append(i[4])

# plt.plot(results)
# plt.show()

data1 = data[:5350]
data2 = data[5351:]

spike = spike.Spike(data2)
momentum = momentum.Momentum(data2)
spike.setExchangeFee(.11)
momentum.setExchangeFee(.11)

# # Strategies

def runSpike(spike):

    spike.setTradeThreshold(2200)
    spike.setInitialInvestment(1000)
    spike.setResolution(50)
    spike.run()
    spike.report()

def runMomentum(momemntum):

    momentum.setTradeThreshold(3250)
    momentum.setInitialInvestment(1000)
    momentum.setResolution(225)
    momentum.run()
    momentum.report()

# runSpike(spike)
# runMomentum(momentum)




# # Run tests

def test_spike(spike):

    spike_test = strategy_test.StrategyTest(spike)
    spike_test.setRange(3000, 4000)
    spike_test.setInterval(500)
    spike_test.testThreshold(resolution = 50)
    spike_test.report()

def test_momentum(momentum):

    momentum_test = strategy_test.StrategyTest(momentum)
    momentum_test.setRange(150, 300)
    momentum_test.setInterval(50)
    momentum_test.testResolution(threshold = 3250)
    momentum_test.report()

# test_spike(spike)
# test_momentum(momemntum)



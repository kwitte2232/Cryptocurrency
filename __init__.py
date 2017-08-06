import os
from os.path import dirname, join
import time
import dotenv

import gather_data
import strategies.momentum as momentum
import strategies.spike as spike
import strategy_test

import matplotlib.pyplot as plt

dotenv.load_dotenv(join(dirname(__file__), '.env'))

# DATA_RESOLUTION = os.environ.get('DATA_RESOLUTION')

# btceth.schedule_rate_pulls(interval=DATA_RESOLUTION)
# time.sleep(1)

btceth = gather_data.GatherData('BTC', 'ETH')

data = btceth.retrieve_exchange_rates();

spike = spike.Spike(data)
momentum = momentum.Momentum(data)
spike.setExchangeFee(.11)
momentum.setExchangeFee(.11)

# # Strategies

# spike.setTradeThreshold(2200)
# spike.setInitialInvestment(1000)
# spike.setResolution(50)
# spike.run()
# spike.report()

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
# spike_test.setInterval(20)
# spike_test.testThreshold(resolution = 50)
# spike_test.report()

if len(results):
    plt.plot(results)
    plt.show()

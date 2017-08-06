import os
from os.path import dirname, join
import time
import dotenv
import sched
import math
import threading

import gather_data
import strategies.spike as strategy

class Trade():

    def __init__(self):

        dotenv.load_dotenv(join(dirname(__file__), '.env'))

        self.PULL_RESOLUTION = int(os.environ.get('PULL_RESOLUTION'))
        self.TEST_RESOLUTION = int(os.environ.get('TEST_RESOLUTION'))

        self.btceth = gather_data.GatherData('BTC', 'ETH')
        self.scheduler = sched.scheduler(time.time, time.sleep)

        self.bought = False
        self.invested_value = 1000
        self.traded_value = 0

    def roundTime(self, timestamp):
        return int(math.floor(timestamp / self.PULL_RESOLUTION) * self.PULL_RESOLUTION)

    def run(self):

        timestamp = self.roundTime(int(time.time()))

        self.btceth.fetch_and_presists_exchange_rate(timestamp=timestamp)
        self.tradeCheck(timestamp=timestamp)

        threading.Timer(self.PULL_RESOLUTION, self.run).start()

        self.scheduler.run()

    def tradeCheck(self, timestamp = None):
        if timestamp == None:
            timestamp = self.roundTime(int(time.time()))

        timestamp -= self.TEST_RESOLUTION

        data = self.btceth.retrieveExchangeRatesSince(timestamp);

        spike = strategy.Spike(data)
        spike.setExchangeFee(.11)
        spike.setTradeThreshold(2200)
        spike.setInitialInvestment(self.invested_value)
        spike.setResolution(self.TEST_RESOLUTION / self.PULL_RESOLUTION)

        # If we don't get enough data, eject!
        if len(data) < self.TEST_RESOLUTION / self.PULL_RESOLUTION * .75:
            print "Insufficient data:", str(len(data)) + "/" + str(self.TEST_RESOLUTION / self.PULL_RESOLUTION), "since", str(timestamp)
            if self.bought:
                value = float(list(data).pop()[4])
                self.bought = False
                self.sell(spike, value)
                spike.report()
            return False

        buy = spike.test()

        if buy and self.bought == False:
            value = float(list(data).pop()[4])
            self.buy(spike, value)
            print "Bought at", value, "for", self.invested_value
        elif buy == False and self.bought:
            value = float(list(data).pop()[4])
            self.sell(spike, value)
            print "Sold at", value, "for", self.invested_value

    def buy(self, spike, value):
        spike.invested_value = self.invested_value
        self.traded_value = spike.buy(value)
        self.bought = True

    def sell(self, spike, value):
        spike.traded_value = self.traded_value
        self.invested_value = spike.sell(value)
        self.bought = False
        spike.report()


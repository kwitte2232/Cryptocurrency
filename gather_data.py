import time
import sched
import math
import requests
import exchange_rate
import threading

class GatherData():

    interval = 60

    def __init__(self, currency_from='BTC', currency_to='ETH'):
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.exchange_rate = exchange_rate.ExchangeRate()
        self.exchange_rate.currency_from = currency_from
        self.exchange_rate.currency_to = currency_to

    def set_interval(self, interval):
        if interval != None:
            self.interval = int(interval)

    def round_time(self, timestamp):
        return int(math.floor(timestamp / self.interval) * self.interval)

    def schedule_rate_pulls(self, iterations=0, interval=None):
        self.set_interval(interval)

        if iterations == 0:
            self.fetch_and_presists_exchange_rate()
            threading.Timer(self.interval, self.schedule_rate_pulls).start()
        else:
            for iteration in range(0, iterations):
                offset = iteration * self.interval
                self.scheduler.enter(offset, 1, self.fetch_and_presists_exchange_rate, [])

        self.scheduler.run()

    def fetch_and_presists_exchange_rate(self):
        timestamp = self.round_time(int(time.time()))
        rate = self.fetch_exchange_rate()
        if rate != False:
            self.persists_exchange_rate(timestamp, rate)
            print rate

    def fetch_exchange_rate(self):
        url = 'https://shapeshift.io/rate/' + self.currency_from.lower() + '_' + self.currency_to.lower()
        response = requests.get(url)
        if 'rate' in response.json():
            return response.json()['rate']
        else:
            print 'Failed to fetch rate:'
            print response.json()

    def persists_exchange_rate(self, timestamp, rate):
        self.exchange_rate.timestamp = timestamp
        self.exchange_rate.rate = rate
        self.exchange_rate.create()

    def retrieve_exchange_rates(self):
        self.exchange_rate.fetchAll()

import time
import sched
import math
import requests
import models.exchange_rate as exchange_rate
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

    def setInterval(self, interval):
        if interval != None:
            self.interval = int(interval)

    def roundTime(self, timestamp):
        return int(math.floor(timestamp / self.interval) * self.interval)

    def scheduleRatePulls(self, iterations=0, interval=None):
        self.setInterval(interval)

        if iterations == 0:
            self.fetchAndPresistExchangeRate()
            threading.Timer(self.interval, self.scheduleRatePulls).start()
        else:
            for iteration in range(0, iterations):
                offset = iteration * self.interval
                self.scheduler.enter(offset, 1, self.fetchAndPresistExchangeRate, [])

        self.scheduler.run()

    def fetchAndPresistExchangeRate(self, timestamp=None):
        if timestamp == None:
            timestamp = self.roundTime(int(time.time()))
        rate = self.fetchExchangeRate()
        if rate != False and rate != None:
            self.persistExchangeRate(timestamp, rate)
            print rate

    def fetchExchangeRate(self):
        url = 'https://shapeshift.io/rate/' + self.currency_from.lower() + '_' + self.currency_to.lower()
        response = requests.get(url)
        if 'rate' in response.json():
            return response.json()['rate']
        else:
            print 'Failed to fetch rate:'
            print response.json()

    def persistExchangeRate(self, timestamp, rate):
        self.exchange_rate.timestamp = timestamp
        self.exchange_rate.rate = rate
        self.exchange_rate.create()

    def retrieveExchangeRates(self):
        return self.exchange_rate.fetchAll(self.currency_from, self.currency_to)

    def retrieveExchangeRatesBetween(self, start, end=None):
        return self.exchange_rate.fetchAllBetween(self.currency_from, self.currency_to, start, end)

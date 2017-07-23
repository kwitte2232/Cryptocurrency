import database
import time
import sched
import math
import requests

class GatherData():

    interval = 60

    def __init__(self, currency_from='BTC', currency_to='ETH'):
        self.initialize_database()
        self.currency_from = currency_from
        self.currency_to = currency_to
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def initialize_database(self):
        self.db = database.Database()
        self.db.query("CREATE TABLE IF NOT EXISTS exchange_rates (id INT AUTO_INCREMENT KEY, timestamp TEXT, currency_from TEXT, currency_to TEXT, rate FLOAT)")

    def set_interval(self, interval):
        if interval != None:
            self.interval = interval

    def round_time(self, timestamp):
        return int(math.floor(timestamp / self.interval) * self.interval)

    def schedule_rate_pulls(self, iterations=0, interval=None):
        self.set_interval(interval)

        if iterations == 0:
            self.scheduler.enter(0, 1, self.fetch_and_presists_exchange_rate, [])
            self.scheduler.enter(self.interval, 1, self.schedule_rate_pulls, [0])
        else:
            for iteration in range(0, iterations):
                offset = iteration * self.interval
                self.scheduler.enter(offset, 1, self.fetch_and_presists_exchange_rate, [])

        self.scheduler.run()

    def fetch_and_presists_exchange_rate(self):
        timestamp = self.round_time(int(time.time()))
        print timestamp
        response = self.fetch_exchange_rate()
        self.persists_exchange_rate(timestamp, response['ticker']['price'])
        print response['ticker']['price']

    def fetch_exchange_rate(self):
        url = 'https://api.cryptonator.com/api/ticker/' + self.currency_from + '-' + self.currency_to
        print url
        response = requests.get(url)
        return response.json()

    def persists_exchange_rate(self, timestamp, rate):
        # timestamp = str(int(time.time()))
        # currency_from = 'BTC'
        # currency_to = 'ETH'
        # rate = 0.000024214
        self.db.query("INSERT INTO exchange_rates (`timestamp`, `currency_from`, `currency_to`, `rate`) VALUES (%s, %s, %s, %s)", (timestamp, self.currency_from, self.currency_to, rate))

    def retrieve_exchange_rates(self):
        self.db.query("SELECT * FROM exchange_rates")

btceth = GatherData('BTC', 'ETH')

# print(gather_data.pull_result(str(int(time.time())), 'BTC', 'ETH'))
btceth.schedule_rate_pulls(3, 3)

print btceth.retrieve_exchange_rates()






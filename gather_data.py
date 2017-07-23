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
        self.db.query('''CREATE TABLE IF NOT EXISTS exchange_rates
            (timestamp text, currency_from text, currency_to text, rate real)''')

    def round_time(self, timestamp, interval):
        return int(math.floor(timestamp / interval) * interval)

    def fetch_exchange_rates(self, iterations=1, interval=None):
        if interval == None:
            interval = self.interval

        timestamp = self.round_time(int(time.time()), interval)

        for iteration in range(0, iterations):
            offset = iteration * interval
            self.scheduler.enter(offset, 1, self.fetch_and_presists_exchange_rate, [])

        self.scheduler.run()

    def fetch_and_presists_exchange_rate(self):
        response = self.fetch_exchange_rate()
        print response['ticker']['price']

    def fetch_exchange_rate(self):
        print int(time.time())
        url = 'https://api.cryptonator.com/api/ticker/' + self.currency_from + '-' + self.currency_to
        print url
        response = requests.get(url)
        return response.json()

    def persists_exchange_rate(self, timestamp, rate):
        # timestamp = str(int(time.time()))
        # currency_from = 'BTC'
        # currency_to = 'ETH'
        # rate = 0.000024214
        result = self.db.cursor.execute("insert into exchange_rates values (?, ?, ?, ?)", (timestamp, self.currency_from, self.currency_to, rate))

btceth = GatherData('BTC', 'ETH')

# print(gather_data.pull_result(str(int(time.time())), 'BTC', 'ETH'))
btceth.fetch_exchange_rates(5)






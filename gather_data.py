import database
import time

class GatherData():

    def __init__(self):
        self.initialize_database()

    def initialize_database(self):
        self.db = database.Database()
        self.db.query('''CREATE TABLE IF NOT EXISTS exchange_rates
            (timestamp text, currency_from text, currency_to text, rate real)''')

    def persists_exchange_rate(self, timestamp, currency_from, currency_to, rate):
        # timestamp = str(int(time.time()))
        # currency_from = 'BTC'
        # currency_to = 'ETH'
        # rate = 0.000024214
        result = self.db.cursor.execute("insert into exchange_rates values (?, ?, ?, ?)", (timestamp, currency_from, currency_to, rate))

gather_data = GatherData()
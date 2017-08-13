import model
import pandas as pd

class Candlestick(model.Model):

    table = 'candlesticks'
    columns = [ 'id', 'timestamp', 'currency_from', 'currency_to', 'high', 'low', 'open', 'close', 'volume', 'quote_volume', 'weighted_average' ]
    fillable = [ 'timestamp', 'currency_from', 'currency_to', 'high', 'low', 'open', 'close', 'volume', 'quote_volume', 'weighted_average' ]

    def initialize(self):
        self.db.query("CREATE TABLE IF NOT EXIST " + self.table + " (id INT AUTO_INCREMENT KEY, timestamp TEXT, currency_from TEXT, currency_to TEXT, high TEXT, low TEXT, open TEXT, close TEXT, volume TEXT, quote_volume TEXT, weighted_average TEXT)")

    def fetchAll(self, currency_from='BTC', currency_to='ETH'):
        return self.makeQuery(self.getSelect() + self.getWhereCurrency(currency_from, currency_to))

    def fetchAllBetween(self, currency_from='BTC', currency_to='ETH', start=0, end=None):
        query = self.getSelect() + self.getWhereCurrency(currency_from, currency_to)
        query += " AND `timestamp` >= " + str(start) + " "

        if end != None:
            query += " AND `timestamp` <= " + str(end) + " "

        return self.makeQuery(query)

    def getWhereCurrency(self, currency_from='BTC', currency_to='ETH'):
        return " WHERE `currency_from` LIKE '"+currency_from+"' AND `currency_to` LIKE '"+currency_to+"' "

    def transformModel(self, dataframe):
        dataframe[['id', 'timestamp', 'high', 'low', 'open', 'close', 'volume']] = dataframe[['id', 'timestamp', 'high', 'low', 'open', 'close', 'volume']].apply(pd.to_numeric)
        dataframe.index = pd.to_datetime(dataframe['timestamp'], unit='s')
        del dataframe.index.name
        return dataframe
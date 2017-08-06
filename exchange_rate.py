import model

class ExchangeRate(model.Model):

    table = 'exchange_rates'
    fillable = [ 'timestamp', 'currency_from', 'currency_to', 'rate' ]

    def initialize(self):
        self.db.query(self.getSelectQuery() + "(id INT AUTO_INCREMENT KEY, timestamp TEXT, currency_from TEXT, currency_to TEXT, rate TEXT)")

    def fetchAll(self, currency_from='BTC', currency_to='ETH'):
        return self.makeQuery(self.getSelect() + self.getWhereCurrency(currency_from, currency_to))

    def fetchAllBetween(self, currency_from='BTC', currency_to='ETH', start=0, end=None):
        query = self.getSelect() + self.getWhereCurrency(currency_from, currency_to)
        query += " AND `timestamp` > " + str(start) + " "

        if end != None:
            query += " AND `timestamp` < " + str(end) + " "

        return self.makeQuery(query)

    def makeQuery(self, query):
        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()

    def getSelect(self):
        return "SELECT * FROM " + self.table + " "

    def getWhereCurrency(self, currency_from='BTC', currency_to='ETH'):
        return " WHERE `currency_from` LIKE '"+currency_from+"' AND `currency_to` LIKE '"+currency_to+"' "
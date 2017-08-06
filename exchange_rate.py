import model

class ExchangeRate(model.Model):

    table = 'exchange_rates'
    fillable = [ 'timestamp', 'currency_from', 'currency_to', 'rate' ]

    def initialize(self):
        self.db.query("CREATE TABLE IF NOT EXISTS "+self.table+" (id INT AUTO_INCREMENT KEY, timestamp TEXT, currency_from TEXT, currency_to TEXT, rate TEXT)")

    def fetchAll(self, currency_from='BTC', currency_to='ETH'):
        self.db.cursor.execute("SELECT * FROM "+self.table+" WHERE `currency_from` LIKE '"+currency_from+"' AND `currency_to` LIKE '"+currency_to+"'")
        return self.db.cursor.fetchall()

    def fetchAllSince(self, currency_from='BTC', currency_to='ETH', timestamp = 0):
        self.db.cursor.execute("""
            SELECT * FROM """+self.table+"""
                WHERE `currency_from` LIKE '"""+currency_from+"""'
                AND `currency_to` LIKE '"""+currency_to+"""'
                AND `timestamp` > """+str(timestamp)+"""
        """)
        return self.db.cursor.fetchall()

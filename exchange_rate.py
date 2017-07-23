import database

class ExchangeRate():

    def __init__(self):
        self.initialize_database()

    def initialize_database(self):
        self.db = database.Database()
        self.db.query("CREATE TABLE IF NOT EXISTS exchange_rates (id INT AUTO_INCREMENT KEY, timestamp TEXT, currency_from TEXT, currency_to TEXT, rate TEXT)")

    def create(self, attributes):
        self.db.query("INSERT INTO exchange_rates (`timestamp`, `currency_from`, `currency_to`, `rate`) VALUES (%s, %s, %s, %s)", attributes)

    def fetchAll(self):
        self.db.cursor.execute('SELECT * FROM exchange_rates')
        return self.db.cursor.fetchall()

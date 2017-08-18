import model
import pandas as pd

class Trade(model.Model):

    table = 'trades'
    columns = [ 'id', 'test_run_id', 'invested_value', 'returned_value', 'buy_time', 'sell_time' ]
    fillable = [ 'test_run_id', 'invested_value', 'returned_value', 'buy_time', 'sell_time' ]

    def initialize(self):
        self.db.query("CREATE TABLE IF NOT EXISTS `" + self.table + "` (id INT AUTO_INCREMENT KEY, `test_run_id` TEXT, `invested_value` TEXT, `returned_value` TEXT, buy_time TEXT, sell_time TEXT)")

    def fetchAll(self):
        return self.makeQuery(self.getSelect())

    def fetch(self, id):
        return self.makeQuery(self.getSelect() + " WHERE `id` LIKE '" + str(id) + "'")

    def fetchForRun(self, id):
        return self.makeQuery(self.getSelect() + " WHERE `test_run_id` LIKE '" + str(id) + "'")

    def transformModel(self, dataframe):
        dataframe[['invested_value', 'returned_value', 'buy_time', 'sell_time']] = dataframe[['invested_value', 'returned_value', 'buy_time', 'sell_time']].apply(pd.to_numeric)
        return dataframe
import model
import pandas as pd

class Trade(model.Model):

    table = 'trades'
    columns = [ 'id', 'test_run_id', 'invested_value', 'returned_value' 'buy_time', 'sell_time' ]
    fillable = [ 'test_run_id', 'invested_value', 'returned_value' 'buy_time', 'sell_time' ]

    def initialize(self):
        self.db.query("CREATE TABLE IF NOT EXISTS `" + self.table + "` (id INT AUTO_INCREMENT KEY, `from_time` TEXT, `to_time` TEXT, investment TEXT, roi TEXT, parameters TEXT)")

    def fetchAll(self):
        return self.makeQuery(self.getSelect())

    def fetch(self, id):
        return self.makeQuery(self.getSelect() + " WHERE `id` LIKE '" + str(id) + "'")

    def transformModel(self, dataframe):
        dataframe[['from_time', 'to_time', 'investment', 'roi']] = dataframe[['from_time', 'to_time', 'investment', 'roi']].apply(pd.to_numeric)
        return dataframe
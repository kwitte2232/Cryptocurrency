import model
import pandas as pd

class TestRun(model.Model):

    table = 'test_runs'
    columns = [ 'id', 'strategy', 'investment', 'roi', 'from_time', 'to_time', 'parameters' ]
    fillable = [ 'strategy', 'investment', 'roi','from_time', 'to_time', 'parameters' ]

    def initialize(self):
        self.db.query("CREATE TABLE IF NOT EXISTS `" + self.table + "` (id INT AUTO_INCREMENT KEY, strategy TEXT, investment TEXT, roi TEXT, `from_time` TEXT, `to_time` TEXT, parameters TEXT)")

    def fetchAll(self):
        return self.makeQuery(self.getSelect())

    def fetch(self, id):
        return self.makeQuery(self.getSelect() + " WHERE `id` LIKE '" + str(id) + "'")

    def transformModel(self, dataframe):
        dataframe[['from_time', 'to_time', 'investment', 'roi']] = dataframe[['from_time', 'to_time', 'investment', 'roi']].apply(pd.to_numeric)
        return dataframe
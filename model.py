import database
import pandas as pd

class Model():

    table = ''
    fillable = []

    def __init__(self):
        self.db = database.Database()

    def get_fillable_attributes(self):
        attributes = []
        for i in range(len(self.fillable)):
            if hasattr(self, self.fillable[i]):
                attributes.append(getattr(self, self.fillable[i]))
            else:
                attributes.append(None)
        return attributes

    def get_fillable_columns(self):
        columns = '`, `'.join(self.fillable)
        columns = '`'+columns+'`'
        return columns

    def create(self):
        attributes = self.get_fillable_attributes()
        columns = self.get_fillable_columns()
        self.db.query("INSERT INTO "+self.table+" ("+columns+") VALUES (%s, %s, %s, %s)", attributes)

    def makeQuery(self, query):
        self.db.cursor.execute(query)
        data = self.db.cursor.fetchall()
        return self.transformModel(pd.DataFrame(list(data), columns=self.columns))

    def getSelect(self):
        return "SELECT * FROM " + self.table + " "

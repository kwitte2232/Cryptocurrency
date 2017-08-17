import database
import pandas as pd

class Model():

    table = ''
    fillable = []

    def __init__(self):
        self.db = database.Database()

    def getFillableAttributes(self):
        attributes = []
        for i in range(len(self.fillable)):
            if hasattr(self, self.fillable[i]):
                attributes.append(getattr(self, self.fillable[i]))
            else:
                attributes.append(None)
        return attributes

    def getFillableColumns(self):
        columns = '`, `'.join(self.fillable)
        columns = '`'+columns+'`'
        return columns

    def create(self):
        attributes = self.getFillableAttributes()
        columns = self.getFillableColumns()
        values = ''
        for column in self.fillable:
            if values == '':
                values += '%s'
            else: 
                values += ', %s'

        print columns, values, attributes

        # print "INSERT INTO "+self.table+" ("+columns+") VALUES ("+values+")", attributes
        self.db.query("INSERT INTO "+self.table+" ("+columns+") VALUES ("+values+")", attributes)
        self.id = self.db.cursor.lastrowid
        return self.makeQuery(self.getSelect() + " WHERE `id` LIKE '" + str(self.id) + "'")

    def update(self):
        attributes = self.getFillableAttributes()
        columns = self.getFillableColumns()
        values = ''
        for column in self.fillable:
            if values == '':
                values += '%s'
            else: 
                values += ', %s'

        return self.makeQuery("UPDATE "+self.table+" ("+columns+") VALUES ("+values+") WHERE `id` LIKE `"+self.id+"`", attributes)

    def makeQuery(self, query):
        self.db.cursor.execute(query)
        data = self.db.cursor.fetchall()
        return self.transformModel(pd.DataFrame(list(data), columns=self.columns))

    def getSelect(self):
        return "SELECT * " + self.fromTable()

    def fromTable(self):
        return " FROM " + self.table + " "

import os
import sqlite3
import MySQLdb

class Database():

    connection = None
    cursor = None

    def __init__(self):

        DB_CONNECTION = os.environ.get('DB_CONNECTION')
        DB_DATABASE = os.environ.get('DB_DATABASE')
        DB_USERNAME = os.environ.get('DB_USERNAME')
        DB_PASSWORD = os.environ.get('DB_PASSWORD')

        if DB_CONNECTION == 'sqlite':
            if DB_DATABASE:
                if not os.path.isfile(DB_DATABASE):
                    dbfile = open(DB_DATABASE,"w+")
                    print('Created file:' + DB_DATABASE)
                self.connection = sqlite3.connect(DB_DATABASE)
            else:
                raise Exception('No database specified')
        elif DB_CONNECTION == 'mysql':
            self.connection = MySQLdb.connect(user=DB_USERNAME, passwd=DB_PASSWORD, db=DB_DATABASE)
            self.cursor = self.connection.cursor()

    def query(self, query, args=None):
        if args == None:
            # print 'make simple query:'
            # print query
            self.cursor.execute(query)
        else:
            # print 'make complex query:'
            # print query
            # print args
            self.cursor.execute(query, args)
        # print 'commit query'
        result = self.connection.commit()
        # print result

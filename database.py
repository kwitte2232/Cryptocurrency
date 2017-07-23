import os
import os.path
from os.path import dirname, join
import dotenv
import sqlite3
import MySQLdb

dotenv.load_dotenv(join(dirname(__file__), '.env'))

DB_CONNECTION = os.environ.get('DB_CONNECTION')
DB_DATABASE = os.environ.get('DB_DATABASE')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

class Database():

    connection = None
    cursor = None

    def __init__(self):
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

    def query(self, query, args=None):
        cursor = self.connection.cursor()
        if args == None:
            cursor.execute(query)
        else:
            cursor.execute(query, args)
        result = self.connection.commit()

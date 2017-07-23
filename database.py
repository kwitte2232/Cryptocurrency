import os
import os.path
from os.path import dirname, join
import dotenv
import sqlite3

dotenv.load_dotenv(join(dirname(__file__), '.env'))

DB_CONNECTION = os.environ.get('DB_CONNECTION')
DB_DATABASE = os.environ.get('DB_DATABASE')

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
                self.cursor = self.connection.cursor()
            else:
                raise Exception('No database specified')

    def query(self, query):
        self.cursor.execute(query)
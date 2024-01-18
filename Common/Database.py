"""
Class to connect to a MySQL database.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
from mysql.connector import connect, Error
from getpass import getpass

class Database:
    """Connect to a MySQL database."""
    log = logging.getLogger('Database')

    def __init__(self, dbname: str):
        """Constructor."""
        self.dbname = dbname
        self.host = 'localhost'
        self.log.info('Constructor for mysql:%s:%s', self.host, self.dbname)
        self.conn = None

    def connect(self, user: str, pwd: str):
        """Connect to the database."""
        if self.conn is not None:
            return
        try:
            self.conn = connect(host=self.host, user=user, password=pwd, database=self.dbname)
            self.log.info('Connected to mysql:%s:%s', self.host, self.dbname)
        except Error as e:
            self.log.error('Failed to connect: %s', e)

    def disconnect(self):
        """Disconnect from database."""
        if self.conn is not None:
            self.log.info('Disconnecting from mysql:%s:%s', self.host, self.dbname)
            self.conn.close()
            self.conn = None

    def fetch(self, sql: str):
        """Fetch records using the specified SQL."""
        self.log.debug('Fetching with SQL: %s', sql)
        if self.conn is None:
            self.log.error('Failed to fetch: not connected to database!')
            return None
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.log.info('Fetched %d records', len(rows))
            return rows

def testDatabase():
    """Simple test case for database connection."""
    dbname = 'herbier'
    db = Database(dbname)
    user = 'nicz'
    pwd = getpass(f'Password for {user}@{dbname}:')
    db.connect(user, pwd)
    sql = 'select * from Location'
    rows = db.fetch(sql)
    for row in rows:
        print(row)
    db.disconnect()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testDatabase()
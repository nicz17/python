"""
Class to connect to a MySQL database.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import io
import datetime
import logging
from mysql.connector import connect, Error
from getpass import getpass
import DateTools


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
        
    def execute(self, sql: str):
        """Insert or update using the specified SQL. Return last inserted idx."""
        self.log.info('Executing SQL: %s', sql)
        idx = None
        if self.conn is None:
            self.log.error('Failed to execute: not connected to database!')
            return
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            self.conn.commit()
            idx = cursor.lastrowid
        return idx
        
class Query():
    """Class for building an SQL query."""
    log = logging.getLogger("Query")

    def __init__(self, name: str):
        """Constructor."""
        self.sio = io.StringIO()
        self.name = name

    def add(self, sql: str):
        """Add some SQL."""
        if len(self.sio.getvalue()) > 0 and sql != ',':
            self.sio.write(' ')
        self.sio.write(sql.strip())
        return self

    def addEscapedString(self, text: str):
        """Escape quotes and add the text with quotes."""
        if text is None or text == '':
            self.add('null')
        else:
            escaped = text.replace("'", "''")
            self.add(f"'{escaped}'")
        return self
    
    def addDate(self, dAt: datetime):
        """Add a datetime in database format."""
        if dAt is None:
            self.add('null')
        else:
            self.add(f"'{DateTools.datetimeToString(dAt, '%Y-%m-%d %H:%M:%S')}'")
        return self
    
    def addBool(self, bValue: bool):
        """Add a bool value in database format."""
        if bValue is None:
            self.add('null')
        else:
            self.add('1' if bValue else '0')
        return self
    
    def addNullableFK(self, fk: int):
        """Add the specified foreign key, or null if negative or None."""
        if fk is None or fk <= 0:
            self.add('null')
        else:
            self.add(f'{fk}')
        return self

    def getSQL(self):
        """Return the accumulated SQL"""
        return self.sio.getvalue()

    def close(self):
        self.sio.close()

    def __str__(self):
        return f'Query for {self.name}'


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

def testQuery():
    """Unit test for Query"""
    Query.log.info("Testing Query")
    obj = Query("SomeTable")
    obj.add('select * from Bleu')
    obj.add('where idxBleu = 42 ')
    obj.add(' order by blName asc')
    obj.log.info(obj)
    obj.log.info(obj.getSQL())
    obj.close() 

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testDatabase()
    testQuery()
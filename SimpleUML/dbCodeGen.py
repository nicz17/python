#!/usr/bin/env python3

"""
 Script to read a MySQL database table structure
 to generate python or C++ stubs.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import getopt
import sys
from Database import *
from SettingsLoader import *
from SimpleUMLClass import *


class DatabaseCodeGen():
    """Parse a MySQL table structure to generate a class."""
    log = logging.getLogger('DatabaseCodeGen')

    def __init__(self, lang: str) -> None:
        """Constructor with language."""
        self.lang = lang
        self.clss: SimpleUMLClass
        self.log.info(self)

    def parse(self, dbName: str, table: str):
        """Parse the specified database table."""
        self.log.info('Parsing %s.%s', dbName, table)

        # Create class object
        if self.lang == 'cpp':
            self.clss = SimpleUMLClassCpp()
        else:
            self.clss = SimpleUMLClassPython()
        self.clss.setName(table)

        # Get table structure from DB
        db = self.connectToDb(dbName)
        sql = f'describe {dbName}.{table}'
        rows = db.fetch(sql)
        for row in rows:
            self.log.info(row)
            fieldName = row[0]
            fieldType = row[1]
            fieldNull = row[2]
            pyType = DatabaseCodeGen.getPythonType(fieldType)
            self.clss.addMember(fieldName, pyType)
            self.clss.addMethod(f'get{fieldName}', None, pyType, False)
        db.disconnect()

        # TODO find the table prefix, adapt names

        # Add the Constructor
        # TODO add it first
        members = []
        for member in self.clss.members:
            members.append(member)
        self.clss.addMethod(table, members, None, False)

        # Write the class
        self.clss.generate()

    def getPythonType(dbType: str):
        """Get the python type for the specified SQL type."""
        type = dbType
        if dbType == 'tinyint(1)':
            type = 'bool'
        if dbType.startswith('varchar'):
            type = 'str'
        return type

    def connectToDb(self, dbName: str):
        """Connect to the specified database."""
        sett = SettingsLoader(None).getSettingsDict()
        db = Database(dbName)
        db.connect(sett['db']['user'], sett['db']['pass'])
        return db

    def __str__(self):
        return f'DatabaseCodeGen for {self.lang}'


def getOptions():
    """Parse program arguments and store them in a dict."""
    dOptions = {'db': 'herbier', 'table': None, 'lang': 'python', 'settings': 'settings.json'}
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:t:l:s:", ["help", "db=", "table=", "lang=", "sett="])
    except getopt.GetoptError:
        print("Invalid options: %s", sys.argv[1:])
    for opt, arg in opts:
        #log.info("Parsing option %s value %s", opt, arg)
        if opt in ('-h', '--help'):
            print('simpleUML.py -h (help) -d (output dir) -f (.uml file) -l (language) -s (settings)')
            sys.exit()
        elif opt in ("-d", "--db"):
            dOptions['db'] = arg
        elif opt in ("-t", "--table"):
            dOptions['table'] = arg
        elif opt in ("-l", "--lang"):
            dOptions['lang'] = arg
        elif opt in ("-s", "--sett"):
            dOptions['settings'] = arg
    return dOptions

def configureLogging():
    """ Configures logging to have timestamped logs at INFO level on stdout. """
    logging.basicConfig(
        format = '%(asctime)s %(levelname)s %(name)s: %(message)s',
        datefmt = '%Y.%m.%d %H:%M:%S',
        level = logging.INFO,
        handlers = [logging.StreamHandler()])
    return logging.getLogger('dbCodeGen')

def main():
    """Main function. Runs the parser."""
    log.info('Welcome to dbCodeGen v' + __version__)
    
    if (dOptions['settings']):
        loader = SettingsLoader(dOptions['settings'])
        loader.loadSettings()
    
    if (dOptions['table']):
        log.info('Parsing table %s to generate %s code', dOptions['table'], dOptions['lang'])
        parser = DatabaseCodeGen(dOptions['lang'])
        parser.parse(dOptions['db'], dOptions['table'])
    else:
        log.error('Please enter a table name with -t')

log = configureLogging()
dOptions = getOptions()
main()

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
import TextTools
from Database import *
from DatabaseField import *
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
        # if self.lang == 'cpp':
        #     self.clss = SimpleUMLClassCpp()
        # else:
        #     self.clss = SimpleUMLClassPython()

        # Create module and class
        module = SimpleUMLPythonModule(TextTools.lowerCaseFirst(table))
        self.clss = SimpleUMLClassPython()
        self.clss.setName(table)
        module.addClass(self.clss)

        # Get table structure from DB
        db = self.connectToDb(dbName)
        sql = f'describe {dbName}.{table}'
        rows = db.fetch(sql)
        fields = []
        for row in rows:
            self.log.info(row)
            fields.append(DatabaseField(row[0], row[1], row[2], row[3]))
        db.disconnect()

        # Find the table prefix
        prefix = self.getPrefix(fields)
        self.log.info('Table prefix is %s', prefix)

        # Add the Constructor
        members = []
        field: DatabaseField
        for field in fields:
            name = field.getPythonName(prefix)
            type = field.getPythonType()
            members.append(SimpleUMLParam(name, type))
        self.clss.addMethod(table, members, None, False)

        # Add getters and setters
        for field in fields:
            name = field.getPythonName(prefix)
            type = field.getPythonType()
            ucName = TextTools.upperCaseFirst(name)
            self.clss.addMember(name, type)
            self.clss.addMethod(f'get{ucName}', None, type, False)
            if not field.isPrimaryKey():
                self.clss.addMethod(f'set{ucName}', [SimpleUMLParam(name, type)], None, False)

        # Write the class
        #self.clss.generate()

        # Generate the Cache class
        module.addClass(self.createCache(table))

        # Write the module
        module.generate()

    def createCache(self, table: str) -> SimpleUMLClassPython:
        """Create a class for caching the table records."""
        name = TextTools.upperCaseFirst(table) + 'Cache'
        self.log.info('Generating %s', name)

        clss = SimpleUMLClassPython()
        clss.setName(name)

        clss.addMethod('load', None, None, False)

        return clss

    def getPrefix(self, fields) -> str:
        """Find the largest common prefix to the specified DB fields."""
        field: DatabaseField
        for len in range(7, 1, -1):
            prefix = ''
            found = True
            for field in fields:
                if not field.isPrimaryKey():
                    if prefix == '':
                        prefix = field.name[:len]
                        self.log.debug('Trying prefix %s', prefix)
                    if not field.name.startswith(prefix):
                        found = False
            if found:
                return prefix
        return ''

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

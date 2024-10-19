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

    def __init__(self, lang: str, table: str) -> None:
        """Constructor with language and database table."""
        self.lang = lang
        self.table = table
        self.prefix = None
        self.fields = []
        self.log.info(self)

    def parse(self, dbName: str):
        """Parse the specified database table."""
        self.log.info('Parsing %s.%s', dbName, self.table)

        # Get table structure from DB
        db = self.connectToDb(dbName)
        sql = f'describe {dbName}.{self.table}'
        rows = db.fetch(sql)
        for row in rows:
            self.log.info(row)
            self.fields.append(DatabaseField(row[0], row[1], row[2], row[3]))
        db.disconnect()

        # Find the table prefix
        self.prefix = self.getPrefix()
        self.log.info('Table prefix is %s', self.prefix)

    def generateModuleModel(self):
        """Generate a python module with the object and cache classes."""
        table = self.table

        # Create module
        module = SimpleUMLPythonModule(TextTools.lowerCaseFirst(table))
        module.addImport('config')
        module.addImport('Database')

        # Generate the Object and Cache classes
        module.addClass(self.generateClassObject())
        module.addClass(self.generateClassCache())

        # Write the module
        module.generate()

    def generateModuleUserInterface(self):
        """Generate a python module with the table and editor classes."""
        table = self.table

        # Create module
        module = SimpleUMLPythonModule(f'module{table}')
        module.addImport('from BaseTable import *')
        module.addImport('BaseWidgets')
        module.addImport(f'from {TextTools.lowerCaseFirst(table)} import {table}, {table}Cache')
        module.setGenerateTests(False)

        # Generate the Table and Editor class
        module.addClass(self.generateClassTable())
        module.addClass(self.generateClassEditor())

        # Write the module
        module.generate()

    def generateClassObject(self) -> SimpleUMLClassPython:
        """Create a class representing the table records."""
        clss = SimpleUMLClassPython()
        clss.setName(self.table)

        # Add the Constructor
        members = []
        field: DatabaseField
        for field in self.fields:
            name = field.getPythonName(self.prefix)
            type = field.getPythonType()
            members.append(SimpleUMLParam(name, type))
        clss.addMethod(self.table, members, None, False)

        # Add getters and setters
        for field in self.fields:
            name = field.getPythonName(self.prefix)
            type = field.getPythonType()
            ucName = TextTools.upperCaseFirst(name)
            clss.addMember(name, type)
            clss.addMethod(f'get{ucName}', None, type, False)
            if not field.isPrimaryKey():
                clss.addMethod(f'set{ucName}', [SimpleUMLParam(name, type)], None, False)

        return clss

    def generateClassCache(self) -> SimpleUMLClassPython:
        """Create a class for caching the table records."""
        name = TextTools.upperCaseFirst(self.table) + 'Cache'
        self.log.info('Generating %s', name)

        # Cache class and its constructor
        clss = SimpleUMLClassPython()
        clss.setName(name)
        clss.addMethod(name, None, None, False)

        # Array to store fetched records
        sCollName = TextTools.lowerCaseFirst(self.table) + 's'
        clss.addMember(sCollName, 'array')

        # Database fetch method
        sFieldNames = ', '.join([field.name for field in self.fields])
        sNameField = f'{self.prefix}Name'
        oLoad = clss.addMethod('load', None, None, False)
        oLoad.setDoc(f'Fetch and store the {self.table} records.')
        oLoad.addCodeLine('db = Database.Database(config.dbName)')
        oLoad.addCodeLine('db.connect(config.dbUser, config.dbPass)')
        oLoad.addCodeLine(f'query = Database.Query("{self.table}")')
        oLoad.addCodeLine(f'query.add("select {sFieldNames} from {self.table}")')
        field: DatabaseField
        for field in self.fields:
            if field.name == sNameField or 'name' in field.name:
                oLoad.addCodeLine(f'query.add(" order by {field.name} asc")')
                break
        oLoad.addCodeLine('rows = db.fetch(query.getSQL())')
        oLoad.addCodeLine('for row in rows:')
        oLoad.addCodeLine(f'    self.{sCollName}.append({self.table}(*row))')
        oLoad.addCodeLine('db.disconnect()')
        oLoad.addCodeLine('query.close()')

        # Find-by-id method
        params = [SimpleUMLParam('idx', 'int')]
        oMeth = clss.addMethod('findById', params, self.table, False)
        oMeth.setDoc(f'Find a {self.table} from its primary key.')
        oMeth.addCodeLine(f'item: {self.table}')
        oMeth.addCodeLine(f'for item in self.{sCollName}:')
        oMeth.addCodeLine('    if item.idx == idx:')
        oMeth.addCodeLine('        return item')
        oMeth.addCodeLine('return None')

        # Find-by-name method
        params = [SimpleUMLParam('name', 'str')]
        oMeth = clss.addMethod('findByName', params, self.table, False)
        oMeth.setDoc(f'Find a {self.table} from its unique name.')
        oMeth.addCodeLine(f'item: {self.table}')
        oMeth.addCodeLine(f'for item in self.{sCollName}:')
        oMeth.addCodeLine('    if item.name == name:')
        oMeth.addCodeLine('        return item')
        oMeth.addCodeLine('return None')

        return clss

    def generateClassTable(self) -> SimpleUMLClassPython:
        """Create a class for displaying records in a table."""
        name = f'{self.table}Table'
        self.log.info('Generating %s', name)
        nameObject = TextTools.lowerCaseFirst(self.table)

        # Table columns
        colNames = [ ]
        field: DatabaseField
        for field in self.fields:
            if not (field.isPrimaryKey() or field.size > 64):
                colNames.append(field.getPythonName(self.prefix))
        sColNames = "', '".join(colNames)

        # Table class
        clss = SimpleUMLClassPython()
        clss.setName(name)
        clss.setSuperClass('BaseTable')

        # Constructor
        params = [SimpleUMLParam('cbkSelect', None)]
        oConstr = clss.addMethod(name, params, None, False)
        oConstr.addCodeLine(f'super().__init__(self.onRowSelection, "{nameObject}s")')
        oConstr.addCodeLine('self.data = []')
        oConstr.addCodeLine('self.cbkSelect = cbkSelect')
        oConstr.addCodeLine(f"self.columns = ('{sColNames}')")

        # createWidgets method
        params = [SimpleUMLParam('parent', 'tk.Frame')]
        oMeth = clss.addMethod('createWidgets', params, None, False)
        oMeth.setDoc('Create user widgets.')
        oMeth.addCodeLine('super().createWidgets(parent, self.columns)')

        return clss

    def generateClassEditor(self) -> SimpleUMLClassPython:
        """Create a class for editing the table records."""
        name = f'{self.table}Editor'
        nameObject = TextTools.lowerCaseFirst(self.table)
        self.log.info('Generating %s', name)

        # Cache class and its constructor
        params = [SimpleUMLParam('cbkSave', None)]
        clss = SimpleUMLClassPython()
        clss.setName(name)
        clss.setSuperClass('BaseWidgets.BaseEditor')
        oConstr = clss.addMethod(name, params, None, False)
        oConstr.addCodeLine('super().__init__(cbkSave)')
        oConstr.addCodeLine(f'self.{nameObject} = None')

        # createWidgets method
        params = [SimpleUMLParam('parent', 'tk.Frame')]
        oMeth = clss.addMethod('createWidgets', params, None, False)
        oMeth.setDoc('Add the editor widgets to the parent widget.')
        oMeth.addCodeLine(f'super().createWidgets(parent, \'{self.table} Editor\')')
        oMeth.addCodeLine('')
        field: DatabaseField
        for field in self.fields:
            if field.isPrimaryKey():
                continue
            nameField = TextTools.upperCaseFirst(field.getPythonName(self.prefix).replace('idx', ''))
            nameWidget = f'wid{nameField}'
            nameGetter = f'{self.table}.get{nameField}'
            oMeth.addCodeLine(f'self.{nameWidget} = self.add{field.getEditionKind()}(\'{nameField}\', {nameGetter})')
        oMeth.addCodeLine('')
        oMeth.addCodeLine('self.createButtons(True, True, False)')
        oMeth.addCodeLine('self.enableWidgets()')

        return clss

    def getPrefix(self) -> str:
        """Find the largest common prefix to the specified DB fields."""
        field: DatabaseField
        for len in range(7, 1, -1):
            prefix = ''
            found = True
            for field in self.fields:
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
        generator = DatabaseCodeGen(dOptions['lang'], dOptions['table'])
        generator.parse(dOptions['db'])
        generator.generateModuleModel()
        generator.generateModuleUserInterface()
    else:
        log.error('Please enter a table name with -t')

log = configureLogging()
dOptions = getOptions()
main()

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
        for field in self.getFields():
            field.setPrefix(self.prefix)

    def getFields(self) -> list[DatabaseField]:
        """Return the parsed database fields."""
        return self.fields

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
        module = SimpleUMLPythonModule(f'module{table}s')
        module.addImport('from BaseTable import *')
        module.addImport('from TabsApp import *')
        module.addImport('BaseWidgets')
        module.addImport(f'from {TextTools.lowerCaseFirst(table)} import {table}, {table}Cache')
        module.setGenerateTests(False)

        # Generate the TabModule, Table and Editor class
        module.addClass(self.generateClassTabModule())
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
        for field in self.getFields():
            name = field.getPythonName()
            type = field.getPythonType()
            members.append(SimpleUMLParam(name, type))
        clss.addMethod(self.table, members, None, False)

        # Add getters and setters
        for field in self.getFields():
            name = field.getPythonName()
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
        oConstr = clss.addMethod(name, None, None, False)
        oConstr.addCodeLine('self.db = Database.Database(config.dbName)')

        # Array to store fetched records
        sCollName = TextTools.lowerCaseFirst(self.table) + 's'
        clss.addMember(sCollName, 'array')

        # getArray method
        oGet = clss.addMethod(f'get{self.table}s', None, f'list[{self.table}]', False)
        oGet.setDoc('Return all objects in cache.')
        oGet.addCodeLine(f'return self.{sCollName}')

        # Database fetch method
        sFieldNames = ', '.join([field.name for field in self.getFields()])
        sNameField = f'{self.prefix}Name'
        oLoad = clss.addMethod('load', None, None, False)
        oLoad.setDoc(f'Fetch and store the {self.table} records.')
        oLoad.addCodeLine('self.db.connect(config.dbUser, config.dbPass)')
        oLoad.addCodeLine(f'query = Database.Query("{self.table}")')
        oLoad.addCodeLine(f'query.add("select {sFieldNames} from {self.table}")')
        for field in self.getFields():
            if field.name == sNameField or 'name' in field.name:
                oLoad.addCodeLine(f'query.add("order by {field.name} asc")')
                break
        oLoad.addCodeLine('rows = self.db.fetch(query.getSQL())')
        oLoad.addCodeLine('for row in rows:')
        oLoad.addCodeLine(f'    self.{sCollName}.append({self.table}(*row))')
        oLoad.addCodeLine('self.db.disconnect()')
        oLoad.addCodeLine('query.close()')

        # Save method
        params = [SimpleUMLParam('obj', self.table)]
        met = clss.addMethod('save', params, None, False)
        met.setDoc(f'Insert or update the specified {self.table} in database.')
        met.addCodeLine('if obj is None:')
        met.addCodeLine("    self.log.error('Undefined object to save!')")
        met.addCodeLine("    return")
        met.addCodeLine('if obj.getIdx() > 0:')
        met.addCodeLine('    self.update(obj)')
        met.addCodeLine('else:')
        met.addCodeLine('    self.insert(obj)')

        # Update method
        met = clss.addMethod('update', params, None, False)
        met.setDoc(f'Update the specified {self.table} in database.')
        met.addCodeLine("self.log.info('Updating %s', obj)")
        met.addCodeLine(f"query = Database.Query('Update {self.table}')")
        met.addCodeLine(f"query.add('Update {self.table} set')")
        for count, field in enumerate(self.getFields()):
            if field.isPrimaryKey(): continue
            isLast = (count == len(self.fields)-1)
            sep = '' if isLast else ".add(',')"
            getter = f'get{TextTools.upperCaseFirst(field.getPythonName())}()'
            if field.isStringValue():
                met.addCodeLine(f"query.add('{field.name} = ').addEscapedString(obj.{getter}){sep}")
            elif field.type == 'datetime':
                met.addCodeLine(f"query.add('{field.name} = ').addDate(obj.{getter}){sep}")
            elif field.getPythonType() == 'bool':
                met.addCodeLine(f"query.add('{field.name} = ').addBool(obj.{getter}){sep}")
            else:
                value = '{obj.' + getter + '}'
                sep = '' if isLast else ','
                met.addCodeLine(f"query.add(f'{field.name} = {value}{sep}')")
        met.addCodeLine("query.add(f'where idx" + self.table + " = {obj.getIdx()}')")
        met.addCodeLine('self.db.connect(config.dbUser, config.dbPass)')
        met.addCodeLine('self.db.execute(query.getSQL())')
        met.addCodeLine('self.db.disconnect()')
        met.addCodeLine('query.close()')

        # Insert method
        met = clss.addMethod('insert', params, None, False)
        met.setDoc(f'Insert the specified {self.table} in database.')
        met.addCodeLine("self.log.info('Inserting %s', obj)")
        met.addCodeLine(f"query = Database.Query('Insert {self.table}')")
        met.addCodeLine(f"query.add('Insert into {self.table} ({sFieldNames})')")
        met.addCodeLine(f"query.add('values (null')")
        for field in self.getFields():
            if field.isPrimaryKey(): continue
            getter = f'get{TextTools.upperCaseFirst(field.getPythonName())}()'
            if field.isStringValue():
                met.addCodeLine(f"query.add(',').addEscapedString(obj.{getter})")
            elif field.type == 'datetime':
                met.addCodeLine(f"query.add(',').addDate(obj.{getter})")
            elif field.getPythonType() == 'bool':
                met.addCodeLine(f"query.add(',').addBool(obj.{getter})")
            else:
                value = '{obj.' + getter + '}'
                met.addCodeLine(f"query.add(f', {value}')")
        met.addCodeLine(f"query.add(')')")
        met.addCodeLine('self.db.connect(config.dbUser, config.dbPass)')
        met.addCodeLine('self.db.execute(query.getSQL())')
        met.addCodeLine('self.db.disconnect()')
        met.addCodeLine('query.close()')
        # TODO get and set generated idx  cursor.lastrowid

        # fetchFromWhere method
        params = [SimpleUMLParam('where', 'str')]
        oFetch = clss.addMethod('fetchFromWhere', params, None, False)
        oFetch.setDoc(f'Fetch {self.table} records from a SQL where-clause. Return a list of ids.')
        oFetch.addCodeLine('result = []')
        oFetch.addCodeLine('self.db.connect(config.dbUser, config.dbPass)')
        oFetch.addCodeLine(f'query = Database.Query("{self.table}")')
        oFetch.addCodeLine(f"query.add('select idx{self.table} from {self.table} where ' + where)")
        oFetch.addCodeLine('rows = self.db.fetch(query.getSQL())')
        oFetch.addCodeLine('result = list(row[0] for row in rows)')
        oFetch.addCodeLine('query.close()')
        oFetch.addCodeLine('self.db.disconnect()')
        oFetch.addCodeLine('return result')

        # Find-by-id method
        params = [SimpleUMLParam('idx', 'int')]
        oMeth = clss.addMethod('findById', params, self.table, False)
        oMeth.setDoc(f'Find a {self.table} from its primary key.')
        oMeth.addCodeLine(f'for item in self.get{self.table}s():')
        oMeth.addCodeLine('    if item.idx == idx:')
        oMeth.addCodeLine('        return item')
        oMeth.addCodeLine('return None')

        # Find-by-name method
        params = [SimpleUMLParam('name', 'str')]
        oMeth = clss.addMethod('findByName', params, self.table, False)
        oMeth.setDoc(f'Find a {self.table} from its unique name.')
        oMeth.addCodeLine(f'for item in self.get{self.table}s():')
        oMeth.addCodeLine('    if item.name == name:')
        oMeth.addCodeLine('        return item')
        oMeth.addCodeLine('return None')

        return clss

    def generateClassTabModule(self) -> SimpleUMLClassPython:
        """Create a TabModule subclass for managing the records."""
        name = f'Module{self.table}s'
        self.log.info('Generating %s', name)
        nameObject = TextTools.lowerCaseFirst(self.table)
        nameCache  = f'{nameObject}Cache'
        nameTable  = f'{self.table}Table'
        nameEditor = f'{self.table}Editor'

        # TabModule subclass
        clss = SimpleUMLClassPython()
        clss.setName(name)
        clss.setSuperClass('TabModule')

        # Constructor
        params = [SimpleUMLParam('parent', 'TabsApp')]
        oConstr = clss.addMethod(name, params, None, False)
        oConstr.addCodeLine('self.window = parent.window')
        oConstr.addCodeLine(f"self.table  = {nameTable}(self.onSelect{self.table})")
        oConstr.addCodeLine(f"self.editor = {nameEditor}(self.onSave{self.table})")
        oConstr.addCodeLine(f"super().__init__(parent, '{self.table}s')")

        # loadData method
        oLoad = clss.addMethod('loadData', None, None, False)
        oLoad.setDoc('Load data from cache and populate table.')
        oLoad.addCodeLine(f'self.{nameCache} = {self.table}Cache()')
        oLoad.addCodeLine(f'self.{nameCache}.load()')
        oLoad.addCodeLine(f'self.table.loadData(self.{nameCache}.get{self.table}s())')

        # onSelectObject method
        params = [SimpleUMLParam(nameObject, self.table)]
        oSel = clss.addMethod(f'onSelect{self.table}', params, None, False)
        oSel.setDoc('Display selected object in editor.')
        oSel.addCodeLine(f'self.editor.loadData({nameObject})')

        # onSaveObject method
        params = [SimpleUMLParam(nameObject, self.table)]
        met = clss.addMethod(f'onSave{self.table}', params, None, False)
        met.setDoc('Save changes to edited object.')
        met.addCodeLine('pass')

        # createWidgets method
        oWid = clss.addMethod('createWidgets', None, None, False)
        oWid.setDoc('Create user widgets.')
        oWid.addCodeLine('self.createLeftRightFrames()')
        oWid.addCodeLine('self.table.createWidgets(self.frmLeft)')
        oWid.addCodeLine('self.editor.createWidgets(self.frmRight)')

        return clss

    def generateClassTable(self) -> SimpleUMLClassPython:
        """Create a class for displaying records in a table."""
        name = f'{self.table}Table'
        self.log.info('Generating %s', name)
        nameObject = TextTools.lowerCaseFirst(self.table)
        nameArray = f'{nameObject}s'

        # Table class
        clss = SimpleUMLClassPython()
        clss.setName(name)
        clss.setSuperClass('TableWithColumns')

        # Constructor
        params = [SimpleUMLParam('cbkSelect', None)]
        oConstr = clss.addMethod(name, params, None, False)
        oConstr.addCodeLine(f'super().__init__(cbkSelect, "{nameArray}")')

        # Table columns
        field: DatabaseField
        for field in self.fields:
            if not (field.isPrimaryKey() or field.size > 64):
                pName = TextTools.upperCaseFirst(field.getPythonName())
                label = field.getLabel()
                width = field.getColumnWidth()
                oConstr.addCodeLine(f"self.addColumn(TableColumn('{label}', {self.table}.get{pName}, {width}))")

        # loadData method
        params = [SimpleUMLParam(nameArray, None)]
        oLoad = clss.addMethod('loadData', params, None, False)
        oLoad.setDoc('Display the specified objects in this table.')
        oLoad.addCodeLine('self.clear()')
        oLoad.addCodeLine(f'self.data = {nameArray}')
        oLoad.addCodeLine(f'self.addRows({nameArray})')

        # createWidgets method
        # params = [SimpleUMLParam('parent', 'tk.Frame')]
        # oMeth = clss.addMethod('createWidgets', params, None, False)
        # oMeth.setDoc('Create user widgets.')
        # oMeth.addCodeLine('super().createWidgets(parent, self.columns)')

        return clss

    def generateClassEditor(self) -> SimpleUMLClassPython:
        """Create a class for editing the table records."""
        name = f'{self.table}Editor'
        nameObject = TextTools.lowerCaseFirst(self.table)
        self.log.info('Generating %s', name)

        # Editor class and its constructor
        params = [SimpleUMLParam('cbkSave', None)]
        clss = SimpleUMLClassPython()
        clss.setName(name)
        clss.setSuperClass('BaseWidgets.BaseEditor')
        oConstr = clss.addMethod(name, params, None, False)
        oConstr.addCodeLine('super().__init__(cbkSave)')
        oConstr.addCodeLine(f'self.{nameObject} = None')

        # loadData method
        params = [SimpleUMLParam(nameObject, self.table)]
        oLoad = clss.addMethod('loadData', params, None, False)
        oLoad.setDoc('Display the specified object in this editor.')
        oLoad.addCodeLine(f'self.{nameObject} = {nameObject}')
        oLoad.addCodeLine(f'self.setValue({nameObject})')

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
            nameField = TextTools.upperCaseFirst(field.getPythonName().replace('idx', ''))
            nameWidget = f'wid{nameField}'
            nameGetter = f'{self.table}.get{nameField}'
            label = field.getLabel()
            oMeth.addCodeLine(f"self.{nameWidget} = self.add{field.getEditionKind()}('{label}', {nameGetter})")
        oMeth.addCodeLine('')
        oMeth.addCodeLine('self.createButtons(True, True, False)')
        oMeth.addCodeLine('self.enableWidgets()')

        # enableWidgets method
        params = [SimpleUMLParam('evt=None')]
        oMeth = clss.addMethod('enableWidgets', params, None, False)
        oMeth.setDoc('Enable or disable widgets of this editor.')
        oMeth.addCodeLine(f'editing  = self.{nameObject} is not None')
        oMeth.addCodeLine(f'modified = self.hasChanges(self.{nameObject})')
        oMeth.addCodeLine('super().enableWidgets(editing)')
        oMeth.addCodeLine('self.enableButtons(modified, modified, False)')

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

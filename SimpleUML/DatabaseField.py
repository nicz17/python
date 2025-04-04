"""Module DatabaseField"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import TextTools


class DatabaseField():
    """Class DatabaseField"""
    log = logging.getLogger("DatabaseField")

    def __init__(self, name: str, type: str, nullable: bool, role: str):
        """Constructor."""
        self.name = name
        self.type = type
        self.role = role
        self.size = 0
        self.nullable = nullable
        self.prefix = None
        if self.type.startswith('varchar('):
            self.size = int(self.type.replace('varchar(', '').replace(')', ''))

    def setPrefix(self, prefix: str):
        self.prefix = prefix

    def getPythonName(self):
        """Get the python name"""
        name = self.name.removeprefix(self.prefix)
        name = TextTools.lowerCaseFirst(name)
        if self.isPrimaryKey():
            return 'idx'
        return name

    def getPythonType(self):
        """Get the python type"""
        type = self.type
        if self.type == 'tinyint(1)':
            type = 'bool'
        if self.type.startswith('varchar'):
            type = 'str'
        return type

    def isStringValue(self):
        """Checks if database requires a string for setting the value."""
        if self.type.startswith('varchar'):
            return True
        return False

    def getEditionKind(self):
        """Guess the kind of widget to use in editor for this field."""
        kind = 'Text'
        ptype = self.getPythonType()
        if ptype == 'int':
            kind = 'IntInput'
        elif ptype == 'bool':
            kind = 'CheckBox'
        elif self.type == 'datetime':
            kind = 'DateTime'
        elif ptype == 'str' and self.size > 100:
            kind = 'TextArea'
        return kind
    
    def getLabel(self):
        """Split camel case into separate words."""
        pname = self.getPythonName()
        label = TextTools.upperCaseFirst(TextTools.splitCamelCase(pname))
        return label
    
    def getColumnWidth(self):
        """Guess the column width in pixels for this field."""
        width = 100
        ptype = self.getPythonType()
        if ptype == 'int':
            width = 80
        elif ptype == 'bool':
            width = 50
        elif self.type == 'datetime':
            width = 160
        elif ptype == 'str':
            width = 4*self.size
        return width

    def isPrimaryKey(self):
        """Check if this field is the table's primary key."""
        return self.role == 'PRI'

    def __str__(self):
        str = f'DatabaseField name: {self.name} type: {self.type}'
        return str


def testDatabaseField():
    """Unit test for DatabaseField"""
    DatabaseField.log.info("Testing DatabaseField")
    prefix = 'prf'
    obj = DatabaseField(f'{prefix}OrderByName', 'int', False, None)
    obj.setPrefix(prefix)
    obj.log.info(obj)
    obj.log.info('Python name: %s',  obj.getPythonName())
    obj.log.info('Python type: %s',  obj.getPythonType())
    obj.log.info('Edition kind: %s', obj.getEditionKind())
    obj.log.info('Label: %s', obj.getLabel())

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testDatabaseField()

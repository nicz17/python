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
        if self.type.startswith('varchar('):
            self.size = int(self.type.replace('varchar(', '').replace(')', ''))

    def getPythonName(self, prefix: str):
        """Get the python name"""
        name = self.name.removeprefix(prefix)
        name = TextTools.lowerCaseFirst(name)
        if self.isPrimaryKey():
            return 'idx'
        return name

    def getPythonType(self):
        """Get the python type"""
        type = self.type
        if self.type == 'tinyint(1)':
            type = 'bool'
        if self.type == 'datetime':
            type = 'float'
        if self.type.startswith('varchar'):
            type = 'str'
        return type

    def getEditionKind(self):
        """Guess the kind of widget to use in editor for this field."""
        kind = 'TextArea'
        ptype = self.getPythonType()
        if ptype == 'int':
            kind = 'IntInput'
        elif ptype == 'bool':
            kind = 'CheckBox'
        elif self.type == 'datetime':
            kind = 'DateTime'
        return kind

    def isPrimaryKey(self):
        """Check if this field is the table's primary key."""
        return self.role == 'PRI'

    def __str__(self):
        str = f'DatabaseField name: {self.name} type: {self.type}'
        return str


def testDatabaseField():
    """Unit test for DatabaseField"""
    DatabaseField.log.info("Testing DatabaseField")
    obj = DatabaseField('prfOrder', 'int', False, None)
    obj.log.info(obj)
    obj.log.info('Python name: %s',  obj.getPythonName('prf'))
    obj.log.info('Python type: %s',  obj.getPythonType())
    obj.log.info('Edition kind: %s', obj.getEditionKind())

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testDatabaseField()

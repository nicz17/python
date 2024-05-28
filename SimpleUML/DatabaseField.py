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

    def getPythonName(self, prefix: str):
        """Get the python name"""
        name = self.name.removeprefix(prefix)
        name = TextTools.lowerCaseFirst(name)
        if self.role == 'PRI':
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

    def __str__(self):
        str = "DatabaseField"
        str += f' name: {self.name}'
        str += f' type: {self.type}'
        str += f' role: {self.role}'
        str += f' size: {self.size}'
        str += f' nullable: {self.nullable}'
        return str


def testDatabaseField():
    """Unit test for DatabaseField"""
    DatabaseField.log.info("Testing DatabaseField")
    obj = DatabaseField('name', 'str', False, None)
    obj.log.info(obj)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testDatabaseField()


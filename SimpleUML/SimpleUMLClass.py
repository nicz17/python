"""
A simple code generator.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import re
import DateTools
import TextTools
from CodeFile import *


class SimpleUMLMethod():
    """Class method representation."""
    log = logging.getLogger('SimpleUMLMethod')

    def __init__(self, name: str, params: str):
        """Constructor"""
        self.name = name
        self.params = params

    def isConstructor(self, className: str):
        """Check if this method is a constructor."""
        return self.name == className

    def isGetter(self):
        """Check if this method is a getter."""
        return self.name.startswith('get')

    def isSetter(self):
        """Check if this method is a setter."""
        return self.name.startswith('set')
    

class SimpleUMLClass():
    """A simple code generator."""
    log = logging.getLogger('SimpleUMLClass')
    dir = 'test'

    def __init__(self) -> None:
        """Constructor."""
        self.log.info('Constructor')
        self.name = None
        self.members = []
        self.methods = []

    def setName(self, name: str):
        """Define the class name."""
        self.name = name

    def addMember(self, name: str, type: str):
        """Add a class member of the specified name and type."""
        self.log.info('Adding member %s type %s', name, type)
        self.members.append(name)

    def addMethod(self, name: str, params: str, type: str):
        """Add a class method of the specified name and type."""
        self.log.info('Adding method %s params %s', name, params)
        self.methods.append(SimpleUMLMethod(name, params))

    def generate(self):
        """Generate the code."""
        pass

class SimpleUMLClassPython(SimpleUMLClass):
    """A simple python code generator."""
    log = logging.getLogger('SimpleUMLClassPython')

    def __init__(self) -> None:
        """Constructor."""
        super().__init__()

    def generate(self):
        """Generate the code."""
        filename = f'{self.dir}/{self.name}.py'
        self.log.info('Generating %s', filename)
        file = CodeFilePython(filename)

        # Header
        year = DateTools.nowAsString('%Y')
        file.addDoc(f'Module {self.name}')
        file.newline()
        file.write('__author__ = "Nicolas Zwahlen"')
        file.write(f'__copyright__ = "Copyright {year} N. Zwahlen"')
        file.write('__version__ = "1.0.0"')
        file.newline()

        # Imports
        file.write('import logging')
        file.newline(2)

        # Class declaration
        file.write(f'class {self.name}():')
        file.addDoc(f'Class {self.name}', 1)
        file.write(f'log = logging.getLogger("{self.name}")', 1)
        file.newline()

        # Constructor
        #file.write('def __init__(self):', 1)
        #file.addDoc('Constructor.', 2)
        #for member in self.members:
        #    file.write(f'self.{member} = None', 2)
        #file.newline()

        # Methods
        method: SimpleUMLMethod
        for method in self.methods:
            params = 'self'
            if len(method.params) > 0:
                params += f', {method.params}'
            definition = f'def {method.name}({params}):'
            if method.isConstructor(self.name):
                file.write(f'def __init__({params}):', 1)
                file.addDoc('Constructor.', 2)
                for member in self.members:
                    if member in params:
                        file.write(f'self.{member} = {member}', 2)
                    else:
                        file.write(f'self.{member} = None', 2)
            elif method.isGetter():
                member = TextTools.lowerCaseFirst(method.name[3:])
                file.write(definition, 1)
                file.addDoc(f'Getter for {member}', 2)
                file.write(f'return self.{member}', 2)
            elif method.isSetter():
                member = TextTools.lowerCaseFirst(method.name[3:])
                file.write(definition, 1)
                file.addDoc(f'Setter for {member}', 2)
                file.write(f'self.{member} = {method.params}', 2)
            else:
                file.write(definition, 1)
                file.addDoc(f'{method.name}', 2)
                file.write('pass', 2)
            file.newline()

        # toString method
        file.write('def __str__(self):', 1)
        file.write(f'str = "{self.name}"', 2)
        for member in self.members:
            file.write(f'str += " {member}: " + self.{member}', 2)
        file.write('return str', 2)
        file.newline(2)

        # Testing method
        file.write(f'def test{self.name}():')
        file.addDoc(f'Unit test for {self.name}', 1)
        file.write('pass', 1)
        file.newline()
        file.write("if __name__ == '__main__':")
        file.write(f'test{self.name}()', 1)
        file.newline()

        file.close()


class SimpleUMLClassCpp(SimpleUMLClass):
    """A simple C++ code generator."""
    log = logging.getLogger('SimpleUMLClassCpp')

    def __init__(self) -> None:
        """Constructor."""
        super().__init__()

    def generate(self):
        """Generate the code."""
        self.buildHeader()
        self.buildBody()

    def buildHeader(self):
        """Create the .h file."""
        filename = f'{self.dir}/{self.name}.h'
        self.log.info('Building %s', filename)
        flag = self.getIncludeFlag()

        file = CodeFile(filename)
        #file.write(self.buildCopyright())
        file.write(f'#ifndef {flag}')
        file.write(f'#define {flag}')
        file.newline()
        file.write(f'class {self.name} ' + '{')
        file.write('public:\n\nprivate:\n\n};')
        file.write(f'#endif // {flag}')
        file.close()

    def buildBody(self):
        """Create the .cc body file."""
        filename = f'{self.dir}/{self.name}.cc'
        self.log.info('Building %s', filename)

        file = CodeFile(filename)
        #file.write(self.buildCopyright())
        file.write(f'#include {self.name}.h')
        file.newline(2)
        for method in self.methods:
            file.write(f'void {self.name}::{method.name}() ' + '{')
            file.newline()
            file.write('}')
            file.newline()
        file.close()

    def getIncludeFlag(self):
        flag = re.sub(r"([A-Z])", r"_\1", self.name).upper() + '_H_'
        self.log.info('include flag: %s', flag)
        return flag


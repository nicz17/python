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


class SimpleUMLMember():
    """Class member representation."""
    log = logging.getLogger('SimpleUMLMethod')

    def __init__(self, name: str, type = None):
        """Constructor"""
        self.name = name
        self.type = type

class SimpleUMLMethod():
    """Class method representation."""
    log = logging.getLogger('SimpleUMLMethod')

    def __init__(self, name: str, params, type: str, isPrivate = True):
        """Constructor"""
        self.name = name
        self.params = params
        if params is None:
            self.params = []
        self.type = type
        self.isPrivate = isPrivate

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

    def addMember(self, name: str, type = None):
        """Add a class member of the specified name and type."""
        self.log.info('Adding member %s type %s', name, type)
        self.members.append(SimpleUMLMember(name, type))

    def addMethod(self, name: str, params, type: str, isPrivate = True):
        """Add a class method of the specified name and type."""
        self.log.info('Adding method %s params %s', name, params)
        self.methods.append(SimpleUMLMethod(name, params, type, isPrivate))

    def getMember(self, name: str) -> SimpleUMLMember:
        """Return the class member with the specified name, or None."""
        for member in self.members:
            if member.name == name:
                return member
        return None
    
    def getMethod(self, name: str) -> SimpleUMLMethod:
        """Return the class method with the specified name, or None."""
        for method in self.methods:
            if method.name == name:
                return method
        return None
    
    def getConstructor(self):
        """Return the default constructor method for this class, or None."""
        return self.getMethod(self.name)

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

        # Methods
        method: SimpleUMLMethod
        for method in self.methods:
            params = 'self'
            for param in method.params:
                member = self.getMember(param)
                if member and member.type:
                    params += f', {member.name}: {member.type}'
                else:
                    params += f', {param}'
            definition = f'def {method.name}({params}):'
            if method.isConstructor(self.name):
                file.write(f'def __init__({params}):', 1)
                file.addDoc('Constructor.', 2)
                for member in self.members:
                    if member.name in params:
                        file.write(f'self.{member.name} = {member.name}', 2)
                    else:
                        file.write(f'self.{member.name} = None', 2)
            elif method.isGetter():
                memberName = TextTools.lowerCaseFirst(method.name[3:])
                member = self.getMember(memberName)
                if member and member.type:
                    definition = f'def {method.name}({params}) -> {member.type}:'
                file.write(definition, 1)
                file.addDoc(f'Getter for {memberName}', 2)
                file.write(f'return self.{memberName}', 2)
            elif method.isSetter():
                member = TextTools.lowerCaseFirst(method.name[3:])
                file.write(definition, 1)
                file.addDoc(f'Setter for {member}', 2)
                file.write(f'self.{member} = {method.params[0]}', 2)
            else:
                file.write(definition, 1)
                file.addDoc(f'{TextTools.upperCaseFirst(method.name)}', 2)
                file.addComment('TODO: implement', 2)
                file.write('pass', 2)
            file.newline()

        # toJson method
        file.write('def toJson(self):', 1)
        file.addDoc(f'Create a dict of this {self.name} for json export.', 2)
        file.write('data = {', 2)
        for member in self.members:
            file.write(f"'{member.name}': self.{member.name},", 3)
        file.write('}', 2)
        file.write('return data', 2)
        file.newline()

        # toString method
        file.write('def __str__(self):', 1)
        file.write(f'str = "{self.name}"', 2)
        for member in self.members:
            #file.write(f'str += " {member.name}: " + self.{member.name}', 2)
            file.write("str += f' " + member.name + ": {self." + member.name + "}'", 2)
        file.write('return str', 2)
        file.newline(2)

        # Testing method
        file.write(f'def test{self.name}():')
        file.addDoc(f'Unit test for {self.name}', 1)
        file.write(f'{self.name}.log.info("Testing {self.name}")', 1)
        constr = self.getConstructor()
        if constr:
            values = []
            for param in constr.params:
                values.append('None')
            svalues = ', '.join(values)
            file.write(f'obj = {self.name}({svalues})', 1)
            file.write('obj.log.info(obj)', 1)
            file.write('obj.log.info(obj.toJson())', 1)
        file.newline()
        file.write("if __name__ == '__main__':")

        file.write('logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",', 1)
        file.write('level=logging.INFO, handlers=[logging.StreamHandler()])', 2)
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

        # Heading
        self.buildCopyright(file, True)
        file.write(f'#ifndef {flag}')
        file.write(f'#define {flag}')
        file.newline()
        file.write(f'class {self.name} ' + '{')

        # Public methods
        file.write('public:')
        file.newline()
        for method in self.methods:
            if not method.isPrivate:
                self.buildDeclaration(file, method)

        # Private methods
        file.write('private:')
        file.newline()
        for method in self.methods:
            if method.isPrivate:
                self.buildDeclaration(file, method)
        file.newline()

        # Private members
        for member in self.members:
            file.write(f'{member.type} {member.name};', 1)
        file.newline()

        # Ending
        file.write('};')
        file.newline()
        file.write(f'#endif // {flag}')
        file.close()

    def buildBody(self):
        """Create the .cc body file."""
        filename = f'{self.dir}/{self.name}.cc'
        self.log.info('Building %s', filename)
        file = CodeFile(filename)

        # Heading
        self.buildCopyright(file, False)
        file.write(f'#include <string>')
        file.write(f'#include "{self.name}.h"')
        file.newline(2)

        # Methods
        method: SimpleUMLMethod
        for method in self.methods:
            self.buildDefinition(file, method)

        file.close()

    def buildDeclaration(self, file: CodeFile, method: SimpleUMLMethod):
        """Writes the method declaration to the header file."""
        docs = []
        type = 'void '
        isConstructor = method.isConstructor(self.name)
        if isConstructor:
            type = ''
            docs.append('Constructor')
        elif method.type:
            type = f'{method.type} '
        docs.append('TODO: document')
        params = ''
        for param in method.params:
            member = self.getMember(param)
            ptype = 'int'
            if member and member.type:
                ptype = member.type
            if len(params) > 0:
                params += ', '
            params += f'{ptype} {param}'
            docs.append(f'@param {param} ')
        if type and not type.startswith('void'):
            docs.append('@return ')
        file.addMultiLineDoc(docs, 1)
        file.write(f'{type}{method.name}({params});', 1)
        file.newline()

    def buildDefinition(self, file: CodeFile, method: SimpleUMLMethod):
        """Writes the method definition to the body file."""
        type = 'void '
        isConstructor = method.isConstructor(self.name)
        if method.type:
            type = f'{method.type} '
        if isConstructor:
            type = ''
        params = ''
        for param in method.params:
            member = self.getMember(param)
            ptype = 'int'
            if member and member.type:
                ptype = member.type
            if len(params) > 0:
                params += ', '
            params += f'{ptype} {param}'
        file.write(f'{type}{self.name}::{method.name}({params}) ' + '{')
        if isConstructor:
            for member in self.members:
                if member.name in params:
                    file.write(f'{member.name} = {member.name};', 1)
                else:
                    file.write(f'{member.name} = nullptr;', 1)
        elif method.isGetter():
            memberName = TextTools.lowerCaseFirst(method.name[3:])
            file.write(f'return {memberName};', 1)
        elif method.isSetter():
            memberName = TextTools.lowerCaseFirst(method.name[3:])
            file.write(f'{memberName} = {method.params[0]};', 1)
        else:
            file.addComment('TODO: implement', 1)
        file.write('}')
        file.newline()

    def buildCopyright(self, file: CodeFile, isHeader: bool):
        """Create the top documentation part."""
        year = DateTools.nowAsString('%Y')
        date = DateTools.nowAsString('%d.%m.%Y')
        lines = [
            f'{self.name}.' + ('h' if isHeader else 'cc'),
            f'Copyright {year} N. Zwahlen',
            f'Created {date}'
        ]
        file.addMultiLineDoc(lines)
        file.newline(2)

    def getIncludeFlag(self):
        flag = re.sub(r"([A-Z])", r"_\1", self.name).upper() + '_H_'
        self.log.info('include flag: %s', flag)
        return flag


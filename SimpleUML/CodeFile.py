"""
Write code to a file.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging

class CodeFile():
    """Write code to a file."""
    log = logging.getLogger('CodeFile')

    def __init__(self, filename: str) -> None:
        """Constructor."""
        self.log.info('Constructor for %s', filename)
        self.file = open(filename, 'w')

    def addComment(self, comment: str, indent = 0):
        """Add a single-line comment."""
        self.write(f'// {comment}', indent)

    def addDoc(self, text: str, indent = 0):
        """Add a single line of documentation."""
        self.write(f'/* {text} */', indent)

    def addMultiLineDoc(self, lines, indent = 0):
        """Add multiple lines of documentation."""
        self.write(f'/**', indent)
        for line in lines:
            self.write(f' * {line}', indent)
        self.write(f' */', indent)

    def newline(self, amount = 1):
        self.file.write('\n' * amount)

    def write(self, line: str, indent = 0):
        self.file.write('\t' * indent + line + '\n')

    def close(self):
        """Close our file."""
        self.file.close()

class CodeFilePython(CodeFile):
    """Write python code to a file."""
    log = logging.getLogger('CodeFilePython')

    def __init__(self, filename: str) -> None:
        """Constructor."""
        super().__init__(filename)

    def addComment(self, comment: str, indent = 0):
        """Add a single-line comment."""
        self.write(f'# {comment}', indent)

    def addDoc(self, text: str, indent = 0):
        """Add a single line of documentation."""
        self.write(f'"""{text}"""', indent)

    def addMultiLineDoc(self, lines, indent = 0):
        """Add multiple lines of documentation."""
        self.write(f'"""', indent)
        for line in lines:
            self.write(f' {line}', indent)
        self.write(f'"""', indent)
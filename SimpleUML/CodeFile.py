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
        self.log.info('Constructor')
        self.file = open(filename, 'w')

    def addDoc(self, text: str, indent = 0):
        self.write(f'"""{text}"""', indent)

    def newline(self, amount = 1):
        self.file.write('\n' * amount)

    def write(self, line: str, indent = 0):
        self.file.write('\t' * indent + line + '\n')

    def close(self):
        """Close our file."""
        self.file.close()
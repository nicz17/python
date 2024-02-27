"""
Export LogBooks to external files.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import DateTools
from LogBook import *
from LogBookTask import *


class Exporter():
    """Export LogBooks to external files."""
    log = logging.getLogger('Exporter')

    def __init__(self) -> None:
        """Constructor"""
        self.log.info('Constructor')
    
    def exportToTextFile(self, book: LogBook, filename: str):
        """Export a LogBook to a text file."""
        self.log.info('Exporting %s to %s', book, filename)

        file = open(filename, 'w')
        nDashes = len(book.name) + 6
        file.write(f'{"-" * nDashes}\n')
        file.write(f'-- {book.name} --\n')
        file.write(f'{"-" * nDashes}\n')
        for task in book:
            file.write(f'\n{task.title}\n')
            file.write(f'{"-" * (len(task.title))}\n')
            file.write(f'-- Created {DateTools.timestampToString(task.created)}\n')
            for step in task:
                file.write(f'- {step.status.name.upper()} {step.text}\n')
        file.close()


def testExporter():
    """Simple unit test."""
    LogBook.initDefaultDir()
    filename = f'{LogBook.dir}ExportTest.txt'
    book = LogBook('Archive')
    exporter = Exporter()
    exporter.exportToTextFile(book, filename)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testExporter()
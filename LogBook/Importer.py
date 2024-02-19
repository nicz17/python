"""
Import LogBooks from external files.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import os
from LogBook import *
from LogBookTask import *
from pathlib import Path


class Importer():
    """Import LogBooks from external files."""
    log = logging.getLogger('Importer')

    def __init__(self) -> None:
        """Constructor"""
        self.log.info('Constructor')
    
    def importFromTextFile(self, filename: str):
        """Import a LogBook from a text file."""
        self.log.info('Importing from %s', filename)

        # Check file exists
        if not os.path.exists(filename):
            self.log.error('File does not exist: %s', filename)
            return
        
        # Create LogBook
        name = os.path.basename(filename).replace('.txt', '')
        book = LogBook(name)
        book.title = f'Imported from {filename}'
        task = None
        
        # Read file
        file = open(filename, 'r')
        for line in file.readlines():
            line = line.rstrip()
            if len(line) == 0 or line.startswith('--'):
                continue
            if line.startswith('- '):
                self.log.info('Step: %s', line[2:])
                if task is not None:
                    task.addStep(LogBookStep(line[2:]))
            else:
                self.log.info('Task: %s', line)
                task = LogBookTask(line)
                book.addTask(task)
        file.close()

        # Save LogBook
        book.save()


def testImporter():
    """Simple unit test."""
    home = str(Path.home())
    filename = f'{home}/Documents/TodoList.txt'
    importer = Importer()
    importer.importFromTextFile(filename)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testImporter()
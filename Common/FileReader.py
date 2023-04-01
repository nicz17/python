"""
Reads a text file line by line.
Iterable, iteration yields a line.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
import os

class FileReader:
    """Read a text file, iterate on lines."""
    log = logging.getLogger(__name__)

    def __init__(self, sFilename: str, sEncoding=None) -> None:
        """Opens the file if it exists."""
        self.oFile = None
        if sEncoding:
            self.log.info('Reading file %s using encoding %s', sFilename, sEncoding)
        else:
            self.log.info('Reading file %s', sFilename)

        if not os.path.exists(sFilename):
            self.log.error('File %s does not exist', sFilename)
        else:
            if sEncoding:
                self.oFile = open(sFilename, 'r', encoding=sEncoding)
            else:
                self.oFile = open(sFilename, 'r')

    def close(self):
        """Closes the file."""
        if self.oFile:
            self.log.info('Closing file %s', self.oFile.name)
            self.oFile.close()

    def __iter__(self):
        if self.oFile is not None:
            iLine = 0
            while True:
                sLine = self.oFile.readline()
                # if sLine is empty, end of file is reached
                if not sLine:
                    break
                else:
                    iLine += 1
                    yield sLine.strip()
            self.log.info('Read %d lines from %s', iLine, self.oFile.name)

    def __str__(self):
        return 'FileReader ' + str(self.oFile)
    
    def __repr__(self):
        return 'FileReader(' + str(self.oFile) + ')'
    

def testFileReader():
    """Simple unit test."""
    reader = FileReader('test.txt')
    for sLine in reader:
        reader.log.info(sLine)
    reader.close()

if __name__ == '__main__':
    logging.basicConfig(format="[%(levelname)s] %(message)s", 
        level=logging.DEBUG, handlers=[logging.StreamHandler()])
    testFileReader()
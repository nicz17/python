"""Module for various quality and consistency checks."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
import os

from picture import Picture, PictureCache


class QualityChecker():
    """Class for various quality and consistency checks."""
    log = logging.getLogger("QualityChecker")

    def __init__(self):
        """Constructor."""
        self.picCache = PictureCache()

    def checkPictureFiles(self):
        """Check picture files exist."""
        nMissing = 0
        for pic in sorted(self.picCache.getPictures(), key=lambda pic: pic.shotAt):
            filename = f'{config.dirPictures}{pic.getFilename()}'
            if not os.path.exists(filename):
                self.log.error('Missing picture file %s', filename)
                self.log.error('  on %s in %s', pic.getShotAt(), pic.getLocationName())
                nMissing += 1
        self.log.info('Found %d missing picture files', nMissing)

    def checkEmptyTaxa(self):
        """Check that each taxon has observations."""
        pass


def testQuality():
    """Unit test for QualityChecker."""
    checker = QualityChecker()
    checker.checkPictureFiles()
    checker.checkEmptyTaxa()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testQuality()
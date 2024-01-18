"""
 Fetch and store Location records from Panorpa database.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
from Database import *


class LocationCache:
    """Fetch and store Location records from Panorpa database."""
    log = logging.getLogger('LocationCache')

    def __init__(self):
        """Constructor."""
        self.log.info('Constructor')
        self.locations = []

    def load(self):
        """Fetch and store the location records."""
        db = Database(config.dbName)
        db.connect(config.dbUser, config.dbPass)
        sql = 'select idxLocation, locName, locDesc, locLatitude, locLongitude from Location'
        rows = db.fetch(sql)
        for row in rows:
            self.log.info(row)
        db.disconnect()


def testLocationCache():
    """Simple test case for LocationCache class."""
    cache = LocationCache()
    cache.load()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testLocationCache()
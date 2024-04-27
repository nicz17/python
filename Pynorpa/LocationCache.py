"""
 Fetch and store Location records from Panorpa database.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
import math
from Database import *


class Location:
    """Container for Panorpa location object."""
    log = logging.getLogger('LocationCache')

    def __init__(self, row):
        """Constructor from fetched row."""
        self.idx    = row[0]
        self.name   = row[1]
        self.desc   = row[2]
        self.lat    = row[3]
        self.lon    = row[4]
        self.alt    = row[5]
        self.region = row[6]

    def getDistance(self, lat: float, lon: float) -> float:
        """Get the distance to another location."""
        return math.sqrt((self.lat - lat) ** 2 + (self.lon - lon) ** 2)

    def __str__(self):
        str = f'Location {self.idx} {self.name}'
        return str
    

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
        sql  = 'select idxLocation, locName, locDesc, locLatitude, locLongitude, locAltitude, locRegion '
        sql += 'from Location order by locName asc'
        rows = db.fetch(sql)
        for row in rows:
            self.log.debug(row)
            loc = Location(row)
            self.locations.append(loc)
            self.log.debug(loc)
        db.disconnect()
        self.log.info('Done loading %s', self)

    def getLocations(self):
        """Returns the fetched locations."""
        return self.locations

    def getClosest(self, lat: float, lon: float) -> Location:
        """Find the closest location in this cache to the specified lat/lon."""
        closest = None
        minDist = 100000
        for loc in self.locations:
            dist = loc.getDistance(lat, lon)
            if dist < minDist:
                closest = loc
                minDist = dist
        return closest

    def __str__(self):
        str = f'LocationCache with {len(self.locations)} locations'
        return str


def testLocationCache():
    """Simple test case for LocationCache class."""
    cache = LocationCache()
    cache.load()
    closest = cache.getClosest(46.52219597, 6.57062216)
    print(closest)
    closest = cache.getClosest(46.6011348, 6.7310774)
    print(closest)


if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testLocationCache()
"""
 Fetch and store Location records from Panorpa database.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
import math
import Database


class Location:
    """Container for Panorpa location object."""
    log = logging.getLogger('LocationCache')

    def __init__(self, row):
        """Constructor from fetched row."""
        self.idx     = row[0]
        self.name    = row[1]
        self.desc    = row[2]
        self.lat     = row[3]
        self.lon     = row[4]
        self.alt     = row[5]
        self.region  = row[6]
        self.zoom    = row[7]
        self.state   = row[8]

    def getIdx(self) -> int:
        """Getter for idx"""
        return self.idx

    def getName(self) -> str:
        """Getter for name"""
        return self.name

    def setName(self, name: str):
        """Setter for name"""
        self.name = name

    def getDesc(self) -> str:
        """Getter for desc"""
        return self.desc

    def setDesc(self, desc: str):
        """Setter for desc"""
        self.desc = desc

    def getKind(self) -> str:
        """Getter for kind"""
        return self.kind

    def setKind(self, kind: str):
        """Setter for kind"""
        self.kind = kind

    def getRegion(self) -> str:
        """Getter for region"""
        return self.region

    def setRegion(self, region: str):
        """Setter for region"""
        self.region = region

    def getState(self) -> str:
        """Getter for state"""
        return self.state

    def getAltitude(self) -> int:
        return self.alt

    def getDistance(self, lat: float, lon: float) -> float:
        """Get the distance to another location."""
        return math.sqrt((self.lat - lat) ** 2 + (self.lon - lon) ** 2)
    
    def getGPSString(self):
        """Get the GPS coordinates as a string."""
        return f'lat {self.lat} lon {self.lon} zoom {self.zoom}'

    def __str__(self):
        str = f'Location {self.idx} {self.name}'
        return str
    

class LocationCache:
    """Singleton to fetch and store Location records from Panorpa database."""
    log = logging.getLogger('LocationCache')
    _instance = None

    def __new__(cls):
        """Create a singleton object."""
        if cls._instance is None:
            cls._instance = super(LocationCache, cls).__new__(cls)
            cls._instance.log.info('Created the LocationCache singleton')
            cls._instance.load()
        return cls._instance

    def __init__(self):
        """Constructor. Unused as all is done in new."""
        pass

    def load(self):
        """Fetch and store the location records."""
        self.locations = []
        db = Database.Database(config.dbName)
        db.connect(config.dbUser, config.dbPass)
        sql = '''select idxLocation, locName, locDesc, locLatitude, locLongitude, 
            locAltitude, locRegion, locMapZoom, locState 
            from Location order by locName asc'''
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
    
    def getById(self, idxLocation: int) -> Location:
        """Get a Location by primary key."""
        for location in self.locations:
            if location.idx == idxLocation:
                return location
        return None

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
    closest = cache.getClosest(46.52219597, 6.57062216)
    cache.log.info(closest)
    closest = cache.getClosest(46.6011348, 6.7310774)
    cache.log.info(closest)
    locById = cache.getById(67)
    cache.log.info(locById)


if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testLocationCache()
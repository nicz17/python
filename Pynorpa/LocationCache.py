"""
 Fetch and store Location records from Panorpa database.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
import geopy.distance

import Database
import appParam
from LatLonZoom import *


class Location:
    """Container for Panorpa location object."""
    log = logging.getLogger('LocationCache')    
    
    def __init__(self, idx: int, name: str, desc: str, lat: float, lon: float, alt: int, region: str, zoom: int, state: str):
        """Constructor."""
        self.idx = idx
        self.name = name
        self.desc = desc
        self.region = region
        self.state = state
        self.lon = lon
        self.lat = lat
        self.alt = alt
        self.zoom = zoom

        self.pictures = []
        self.excursions = []

    def addPicture(self, picture):
        """Add a picture to this location."""
        if picture:
            self.pictures.append(picture)
    
    def getPictures(self) -> list:
        """Get the pictures of this location."""
        return self.pictures

    def addExcursion(self, excursion):
        """Add an excursion to this location."""
        if excursion:
            self.excursions.append(excursion)
    
    def getExcursions(self) -> list:
        """Get the excursions of this location."""
        return self.excursions

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

    def setAltitude(self, altitude: int):
        """Setter for altitude"""
        self.alt = altitude
    
    def getLatLonZoom(self):
        """Get the lat/lon/zoom triplet."""
        return LatLonZoom(self.lat, self.lon, self.zoom)
    
    def setLatLonZoom(self, llz: LatLonZoom):
        """Set the lat/lon/zoom triplet."""
        if llz:
            self.lat  = llz.getLat()
            self.lon  = llz.getLon()
            self.zoom = llz.getZoom()

    def getDistance(self, lat: float, lon: float) -> float:
        """Get the distance to another location in meters."""
        return 1000*geopy.distance.geodesic((self.lat, self.lon), (lat, lon)).km
    
    def getGPSString(self):
        """Get the GPS coordinates as a string."""
        return self.getLatLonZoom().toPrettyString()

    def __str__(self):
        return f'Location {self.idx} {self.name} ({self.alt}m)'
    

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
        self.db = Database.Database(config.dbName)
        self.db.connect(config.dbUser, config.dbPass)
        query = Database.Query("Locations fetch")
        query.add('select idxLocation, locName, locDesc, locLatitude, locLongitude,')
        query.add('locAltitude, locRegion, locMapZoom, locState')
        query.add('from Location order by locName asc')
        rows = self.db.fetch(query.getSQL())
        for row in rows:
            self.locations.append(Location(*row))
        self.db.disconnect()
        query.close()
        self.log.info('Done loading %s', self)

    def save(self, obj: Location):
        """Insert or update the specified Location in database."""
        if obj is None:
            self.log.error('Undefined object to save!')
            return
        if obj.getIdx() > 0:
            self.update(obj)
        else:
            self.insert(obj)

    def update(self, location: Location):
        """Update the location in database."""
        self.log.info('Updating %s', location)
        query = Database.Query("Location save")
        query.add(f'update Location set')
        query.add('locDesc = ').addEscapedString(location.getDesc()).add(',')
        query.add('locRegion = ').addEscapedString(location.getRegion()).add(',')
        query.add('locState = ').addEscapedString(location.getState()).add(',')
        query.add(f'locAltitude = {location.getAltitude()},')
        query.add(f'locMapZoom = {location.getLatLonZoom().getZoom()}')
        query.add(f'where idxLocation = {location.getIdx()}')
        self.db.connect(config.dbUser, config.dbPass)
        self.db.execute(query.getSQL())
        self.db.disconnect()
        query.close()
        self.log.info('Saved %s', location)

    def insert(self, obj: Location):
        """Insert the specified Location in database."""
        self.log.info('Inserting %s', obj)
        query = Database.Query('Insert Location')
        query.add('Insert into Location (idxLocation, locName, locDesc, locKind, locRegion, locState, ')
        query.add('locLongitude, locLatitude, locAltitude, locMapZoom) values (null')
        query.add(',').addEscapedString(obj.getName())
        query.add(',').addEscapedString(obj.getDesc())
        query.add(',').addEscapedString(obj.getKind())
        #query.add(',').addEscapedString(obj.getTown())
        query.add(',').addEscapedString(obj.getRegion())
        query.add(',').addEscapedString(obj.getState())
        query.add(f', {obj.getLatLonZoom().getLon()}')
        query.add(f', {obj.getLatLonZoom().getLat()}')
        query.add(f', {obj.getAltitude()}')
        query.add(f', {obj.getLatLonZoom().getZoom()}')
        query.add(')')
        self.db.connect(config.dbUser, config.dbPass)
        idx = self.db.execute(query.getSQL())
        self.db.disconnect()
        query.close()
        if idx:
            self.log.info(f'Inserted with idx {idx}')
            obj.idx = idx
            self.locations.append(obj)
        else:
            self.log.error('No idx after insertion!')

    def getLocations(self) -> list[Location]:
        """Returns the fetched locations."""
        return self.locations
    
    def getById(self, idxLocation: int) -> Location:
        """Get a Location by primary key."""
        for location in self.locations:
            if location.idx == idxLocation:
                return location
        return None

    def getByName(self, name: str) -> Location:
        """Find a Location from its unique name."""
        for loc in self.getLocations():
            if loc.name == name:
                return loc
        return None

    def getClosest(self, lat: float, lon: float) -> Location:
        """Find the closest location in this cache to the specified lat/lon."""
        if lat is None or lon is None:
            return None
        closest = None
        minDist = 100000
        for loc in self.getLocations():
            dist = loc.getDistance(lat, lon)
            if dist < minDist:
                closest = loc
                minDist = dist
        return closest
    
    def getDefaultLocation(self) -> Location:
        """Get the current default location from AppParam defLocation."""
        apCache = appParam.AppParamCache()
        apDefLoc = apCache.findByName('defLocation')
        if apDefLoc:
            return self.getById(apDefLoc.getIntVal())
        self.log.error('Failed to find default location AppParam')

    def __str__(self):
        return f'LocationCache with {len(self.locations)} locations'


def testLocationCache():
    """Simple test case for LocationCache class."""
    cache = LocationCache()
    closest = cache.getClosest(46.52219597, 6.57062216)
    cache.log.info(closest)
    closest = cache.getClosest(46.6011348, 6.7310774)
    cache.log.info(closest)
    locById = cache.getById(67)
    cache.log.info(locById)
    defloc = cache.getDefaultLocation()
    cache.log.info('Default location: %s', defloc)


if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testLocationCache()
"""Module picture"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import config
import random
import Database
from taxon import Taxon, TaxonCache
from LocationCache import *
from PhotoInfo import PhotoInfo
import TextTools

class Picture():
    """Class Picture"""
    log = logging.getLogger("Picture")

    def __init__(self, idx: int, filename: str, shotAt: float, remarks: str, 
                 idxTaxon: int, updatedAt: float, idxLocation: int, rating: int):
        """Constructor."""
        self.idx = idx
        self.filename = filename
        self.shotAt = shotAt
        self.remarks = remarks
        self.idxTaxon = idxTaxon
        self.updatedAt = updatedAt
        self.idxLocation = idxLocation
        self.rating = rating
        self.location = None
        self.taxon = None
        self.info = None

    def getIdx(self) -> int:
        """Getter for idx"""
        return self.idx

    def getFilename(self) -> str:
        """Getter for filename"""
        return self.filename

    def setFilename(self, filename: str):
        """Setter for filename"""
        self.filename = filename

    def getShotAt(self) -> float:
        """Getter for shotAt"""
        return self.shotAt

    def setShotAt(self, shotAt: float):
        """Setter for shotAt"""
        self.shotAt = shotAt

    def getLocationName(self) -> str:
        """Get location name"""
        if self.location:
            return self.location.getName()
        return 'Error: undefined location'
    
    def getLocation(self) -> Location:
        """Get the location object."""
        return self.location

    def getRemarks(self) -> str:
        """Getter for remarks"""
        return self.remarks

    def setRemarks(self, remarks: str):
        """Setter for remarks"""
        self.remarks = remarks

    def getIdxTaxon(self) -> int:
        """Getter for taxon"""
        return self.taxon

    def setIdxTaxon(self, idxTaxon: int):
        """Setter for taxon"""
        self.idxTaxon = idxTaxon

    def getTaxonName(self) -> str:
        """Get taxon name"""
        if self.taxon:
            return self.taxon.getName()
        return 'Error: undefined taxon'
    
    def getTaxon(self):
        return self.taxon

    def getUpdatedAt(self) -> float:
        """Getter for updatedAt"""
        return self.updatedAt

    def setUpdatedAt(self, updatedAt: float):
        """Setter for updatedAt"""
        self.updatedAt = updatedAt

    def getIdxLocation(self) -> int:
        """Getter for idxLocation"""
        return self.idxLocation

    def setIdxLocation(self, idxLocation: int):
        """Setter for idxLocation"""
        self.idxLocation = idxLocation

    def getRating(self) -> int:
        """Getter for rating"""
        return self.rating

    def setRating(self, rating: int):
        """Setter for rating"""
        self.rating = rating

    def getPhotoInfo(self) -> PhotoInfo:
        """Get the PhotoInfo object for this picture."""
        if not self.info:
            self.info = PhotoInfo(f'{config.dirPictures}{self.filename}')
            self.info.identify()
        return self.info
        
    def getCloseTo(self) -> str:
        """Get info about location and GPS data."""
        info = self.getPhotoInfo()
        if info and info.hasGPSData():
            dist = self.getLocation().getDistance(info.lat, info.lon)
            return f'{self.getLocationName()} (à {TextTools.distanceToString(dist)})'
        else:
            return f'{self.getLocationName()} (sans données GPS)'

    def toJson(self):
        """Create a dict of this Picture for json export."""
        data = {
            'idx': self.idx,
            'filename': self.filename,
            'shotAt': self.shotAt,
            'remarks': self.remarks,
            'taxon': self.taxon,
            'updatedAt': self.updatedAt,
            'idxLocation': self.idxLocation,
            'rating': self.rating
        }
        return data

    def __str__(self):
        str = f'Picture {self.idx} {self.filename} shotAt: {self.shotAt} idxLocation: {self.idxLocation} rating: {self.rating}'
        return str


class PictureCache():
    """Singleton class to fetch Picture records from database and cache them."""
    log = logging.getLogger("PictureCache")
    _instance = None

    def __new__(cls):
        """Create a singleton object."""
        if cls._instance is None:
            cls._instance = super(PictureCache, cls).__new__(cls)
            cls._instance.log.info('Created the PictureCache singleton')
            cls._instance.load()
        return cls._instance

    def __init__(self):
        """Constructor. Unused as all is done in new."""
        pass

    def getPictures(self) -> list[Picture]:
        """Return all objects in cache."""
        return self.pictures
    
    def getForTaxon(self, idxTaxon) -> list[Picture]:
        """Return all pictures of the specified taxon."""
        result = []
        pic: Picture
        for pic in self.pictures:
            if pic.idxTaxon == idxTaxon:
                result.append(pic)
        return result

    def load(self):
        """Fetch and store the Picture records."""
        self.db = Database.Database(config.dbName)
        self.taxonCache = TaxonCache()
        self.locationCache = LocationCache()
        self.pictures = []

        self.db.connect(config.dbUser, config.dbPass)
        query = Database.Query("Picture")
        query.add("select idxPicture, picFilename, picShotAt, picRemarks, picTaxon, picUpdatedAt, picIdxLocation, picRating")
        query.add("from Picture order by picFilename asc")
        rows = self.db.fetch(query.getSQL())
        for row in rows:
            self.pictures.append(Picture(*row))
        self.db.disconnect()
        query.close()

        # Set picture locations and taxa
        pic: Picture
        for pic in self.pictures:
            pic.location = self.locationCache.getById(pic.idxLocation)
            pic.taxon = self.taxonCache.findById(pic.idxTaxon)
            if pic.taxon:
                pic.taxon.addPicture(pic)
            if pic.location:
                pic.location.addPicture(pic)

    def getLatest(self, limit=10) -> list[Picture]:
        """Get the latest pictures."""
        ids = self.fetchFromWhere(f'1=1 order by picShotAt desc limit {limit}')
        return [self.findById(id) for id in ids]
    
    def getRandomBest(self, limit=8) -> list[Picture]:
        """Get a random list of the best pictures."""
        ids = self.fetchFromWhere(f'picRating = 5')
        random.shuffle(ids)
        return [self.findById(id) for id in ids[:limit]]
    
    def getForExcursion(self, idxLocation: int, tFrom, tTo) -> list[Picture]:
        """Get the pictures for the specified location and date-range."""
        where = f"picIdxLocation = {idxLocation} and picShotAt >= '{tFrom}' and picShotAt <= '{tTo}'"
        ids = self.fetchFromWhere(where)
        return [self.findById(id) for id in ids]

    def fetchFromWhere(self, where: str) -> list[int]:
        """Fetch Picture records from a SQL where-clause. Return a list of ids."""
        result = []
        self.db.connect(config.dbUser, config.dbPass)
        query = Database.Query("Picture")
        query.add(f'select idxPicture from Picture where {where}')
        rows = self.db.fetch(query.getSQL())
        result = list(row[0] for row in rows)
        query.close()
        self.db.disconnect()
        return result

    def findById(self, idx: int) -> Picture:
        """Find a Picture from its primary key."""
        item: Picture
        for item in self.pictures:
            if item.idx == idx:
                return item
        return None

    def findByName(self, name: str) -> Picture:
        """Find a Picture from its unique name."""
        item: Picture
        for item in self.pictures:
            if item.filename == name:
                return item
        return None

    def __str__(self):
        return 'PictureCache'


def testPicture():
    """Unit test for Picture"""
    Picture.log.info("Testing Picture")
    obj = Picture(42, "filenameExample", 3.14, "remarksExample", 42, 3.14, 42, 42)
    obj.log.info(obj)
    obj.log.info(obj.toJson())

def testPictureCache():
    """Unit test for PictureCache"""
    PictureCache.log.info("Testing PictureCache")
    cache = PictureCache()
    latest = cache.getLatest(5)
    for pic in latest:
        cache.log.info(pic)
    best = cache.getRandomBest(5)
    for pic in best:
        cache.log.info(pic)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testPicture()
    testPictureCache()

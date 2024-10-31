"""Module picture"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import config
import Database
from taxon import Taxon, TaxonCache


class Picture():
    """Class Picture"""
    log = logging.getLogger("Picture")

    def __init__(self, idx: int, filename: str, shotAt: float, remarks: str, idxTaxon: int, updatedAt: float, idxLocation: int, rating: int):
        """Constructor."""
        self.idx = idx
        self.filename = filename
        self.shotAt = shotAt
        self.remarks = remarks
        self.idxTaxon = idxTaxon
        self.updatedAt = updatedAt
        self.idxLocation = idxLocation
        self.rating = rating
        self.taxon = None

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
        return 'Not implemented yet'
        #return self.location.name

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
            'rating': self.rating,
        }
        return data

    def __str__(self):
        str = f'Picture {self.idx} {self.filename} shotAt: {self.shotAt} idxLocation: {self.idxLocation} rating: {self.rating}'
        return str


class PictureCache():
    """Class PictureCache"""
    log = logging.getLogger("PictureCache")

    def __init__(self):
        """Constructor."""
        self.db = Database.Database(config.dbName)
        self.taxonCache = TaxonCache()
        self.pictures = []

    def getPictures(self):
        """Return all objects in cache."""
        return self.pictures

    def load(self):
        """Fetch and store the Picture records."""
        self.db.connect(config.dbUser, config.dbPass)
        query = Database.Query("Picture")
        query.add("select idxPicture, picFilename, picShotAt, picRemarks, picTaxon, picUpdatedAt, picIdxLocation, picRating")
        query.add("from Picture order by picFilename asc")
        rows = self.db.fetch(query.getSQL())
        for row in rows:
            self.pictures.append(Picture(*row))
        self.db.disconnect()
        query.close()

        # Set picture taxa
        pic: Picture
        for pic in self.pictures:
            taxon = self.taxonCache.findById(pic.idxTaxon)
            pic.taxon = taxon

    def fetchFromWhere(self, where: str):
        """Fetch Picture records from a SQL where-clause. Return a list of ids."""
        result = []
        self.db.connect(config.dbUser, config.dbPass)
        query = Database.Query("Picture")
        query.add('select idxPicture from Picture where ' + where)
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

    def toJson(self):
        """Create a dict of this PictureCache for json export."""
        data = {
            'pictures': self.pictures,
        }
        return data

    def __str__(self):
        str = 'PictureCache'
        return str


def testPicture():
    """Unit test for Picture"""
    Picture.log.info("Testing Picture")
    obj = Picture(42, "filenameExample", 3.14, "remarksExample", 42, 3.14, 42, 42)
    obj.log.info(obj)
    obj.log.info(obj.toJson())

def testPictureCache():
    """Unit test for PictureCache"""
    PictureCache.log.info("Testing PictureCache")
    obj = PictureCache()
    obj.log.info(obj)
    obj.log.info(obj.toJson())

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testPicture()
    testPictureCache()

"""Module expedition"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import config
import Database
from LocationCache import Location, LocationCache
from picture import Picture, PictureCache
from Timer import Timer
from datetime import datetime

class Expedition():
    """Class Expedition"""
    log = logging.getLogger("Expedition")

    def __init__(self, idx: int, name: str, desc: str, idxLocation: int, tfrom: datetime, to: datetime, track: str):
        """Constructor."""
        self.idx = idx
        self.name = name
        self.desc = desc
        self.idxLocation = idxLocation
        self.tfrom = tfrom
        self.to = to
        self.track = track

        self.location = None
        self.pictures = []

    def addPicture(self, picture):
        """Add a picture to this excursion."""
        if picture:
            self.pictures.append(picture)
    
    def getPictures(self) -> list[Picture]:
        """Get the pictures of this excursion."""
        return self.pictures

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

    def getIdxLocation(self) -> int:
        """Getter for idxLocation"""
        return self.idxLocation

    def setIdxLocation(self, idxLocation: int):
        """Setter for idxLocation"""
        self.idxLocation = idxLocation

    def getLocation(self) -> Location:
        """Getter for Location"""
        return self.location

    def setLocation(self, location: Location):
        """Setter for Location"""
        self.location = location

    def getLocationName(self) -> str:
        """Get the location name"""
        if self.location:
            return self.location.getName()
        return 'Inconnu'

    def getFrom(self) -> datetime:
        """Getter for from"""
        return self.tfrom

    def setFrom(self, tfrom: datetime):
        """Setter for from"""
        self.tfrom = tfrom

    def getTo(self) -> datetime:
        """Getter for to"""
        return self.to

    def setTo(self, to: datetime):
        """Setter for to"""
        self.to = to

    def getTrack(self) -> str:
        """Getter for track"""
        return self.track

    def setTrack(self, track: str):
        """Setter for track"""
        self.track = track

    def getDuration(self) -> float:
        """Get the excursion duration in seconds."""
        if self.tfrom is not None and self.to is not None:
            return self.to.timestamp() - self.tfrom.timestamp()
        return None

    def toJson(self):
        """Create a dict of this Expedition for json export."""
        data = {
            'idx': self.idx,
            'name': self.name,
            'desc': self.desc,
            'idxLocation': self.idxLocation,
            'from': self.tfrom,
            'to': self.to,
            'track': self.track
        }
        return data

    def __str__(self):
        return f'Expedition idx: {self.idx} name: {self.name} date: {self.tfrom}'


class ExpeditionCache():
    """Singleton class for caching Expeditions."""
    log = logging.getLogger("ExpeditionCache")
    _instance = None

    def __new__(cls):
        """Create a singleton object."""
        if cls._instance is None:
            cls._instance = super(ExpeditionCache, cls).__new__(cls)
            cls._instance.log.info('Created the ExpeditionCache singleton')
            cls._instance.load()
        return cls._instance

    def __init__(self):
        """Constructor. Unused as all is done in new."""
        pass

    def getExpeditions(self) -> list[Expedition]:
        """Return all objects in cache."""
        return self.expeditions

    def load(self):
        """Fetch and store the Expedition records."""
        self.db = Database.Database(config.dbName)
        self.locationCache = LocationCache()
        self.pictureCache  = PictureCache()
        self.expeditions = []
        self.db.connect(config.dbUser, config.dbPass)
        query = Database.Query("Expedition")
        query.add("select idxExpedition, expName, expDesc, expLocation, expFrom, expTo, expTrack from Expedition")
        query.add("order by expFrom desc")
        rows = self.db.fetch(query.getSQL())
        for row in rows:
            self.expeditions.append(Expedition(*row))
        self.db.disconnect()
        query.close()

        # Set locations and pictures
        for exped in self.getExpeditions():
            location = self.locationCache.getById(exped.getIdxLocation())
            self.setLocationPictures(exped, location)

    def setLocationPictures(self, exped: Expedition, location: Location):
        """Add pictures from the specified location."""
        if location:
            exped.setLocation(location)
            location.addExcursion(exped)
            picture: Picture
            for picture in location.getPictures():
                if picture.getShotAt() >= exped.getFrom() and picture.getShotAt() <= exped.getTo():
                    exped.addPicture(picture)
            exped.pictures = sorted(exped.pictures, key=lambda pic: pic.shotAt)

    def save(self, obj: Expedition):
        """Insert or update the specified Expedition in database."""
        if obj is None:
            self.log.error('Undefined object to save!')
            return
        if obj.getIdx() > 0:
            self.update(obj)
        else:
            self.insert(obj)

    def update(self, obj: Expedition):
        """Update the specified Expedition in database."""
        self.log.info('Updating %s', obj)
        query = Database.Query('Update Expedition')
        query.add('Update Expedition set')
        query.add('expName = ').addEscapedString(obj.getName()).add(',')
        query.add('expDesc = ').addEscapedString(obj.getDesc()).add(',')
        #query.add(f'expLocation = {obj.getIdxLocation()},')
        query.add('expFrom = ').addDate(obj.getFrom()).add(',')
        query.add('expTo = ').addDate(obj.getTo()).add(',')
        query.add('expTrack = ').addEscapedString(obj.getTrack())
        query.add(f'where idxExpedition = {obj.getIdx()}')
        self.db.connect(config.dbUser, config.dbPass)
        self.db.execute(query.getSQL())
        self.db.disconnect()
        query.close()

    def insert(self, obj: Expedition):
        """Insert the specified Expedition in database."""
        self.log.info('Inserting %s', obj)
        query = Database.Query('Insert Expedition')
        query.add('Insert into Expedition (idxExpedition, expName, expDesc, expLocation, expFrom, expTo, expTrack)')
        query.add('values (null')
        query.add(',').addEscapedString(obj.getName())
        query.add(',').addEscapedString(obj.getDesc())
        query.add(f', {obj.getIdxLocation()}')
        query.add(',').addDate(obj.getFrom())
        query.add(',').addDate(obj.getTo())
        query.add(',').addEscapedString(obj.getTrack())
        query.add(')')
        self.db.connect(config.dbUser, config.dbPass)
        idx = self.db.execute(query.getSQL())
        #self.log.info('Insert SQL: %s', query.getSQL())
        self.db.disconnect()
        query.close()
        if idx:
            self.log.info(f'Inserted with idx {idx}')
            obj.idx = idx
            self.expeditions.append(obj)
            # TODO sort by tFrom desc
        else:
            self.log.error('No idx after insertion!')

    def fetchFromWhere(self, where: str):
        """Fetch Expedition records from a SQL where-clause. Return a list of ids."""
        result = []
        self.db.connect(config.dbUser, config.dbPass)
        query = Database.Query("Expedition")
        query.add('select idxExpedition from Expedition where ' + where)
        rows = self.db.fetch(query.getSQL())
        result = list(row[0] for row in rows)
        query.close()
        self.db.disconnect()
        return result
    
    def fetchMostRecent(self, nMax: int) -> list[Expedition]:
        """Fetch the most recent excursions."""
        where = f'1 == 1 order by expFrom desc limit {nMax}'
        ids = self.fetchFromWhere(where)
        return [self.findById(id) for id in ids]

    def findById(self, idx: int) -> Expedition:
        """Find an Expedition from its primary key."""
        for item in self.getExpeditions():
            if item.idx == idx:
                return item
        return None

    def findByName(self, name: str) -> Expedition:
        """Find an Expedition from its unique name."""
        for item in self.getExpeditions():
            if item.name == name:
                return item
        return None

    def __str__(self):
        return 'ExpeditionCache'


def testExpedition():
    """Unit test for Expedition"""
    Expedition.log.info("Testing Expedition")
    obj = Expedition(42, "nameExample", "descExample", 42, 3.14, 3.14, "trackExample")
    obj.log.info(obj)
    obj.log.info(obj.toJson())

def testExpeditionCache():
    """Unit test for ExpeditionCache"""
    ExpeditionCache.log.info("Testing ExpeditionCache")
    timer = Timer()
    cache = ExpeditionCache()
    cache.log.info('Loaded cache in %s', timer.getElapsed())
    for excursion in cache.getExpeditions():
        cache.log.info(excursion)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testExpedition()
    testExpeditionCache()

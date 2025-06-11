"""Module for managing AppParam records."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import logging
import config
from datetime import datetime
import Database


class AppParam():
    """Class AppParam"""
    log = logging.getLogger("AppParam")

    def __init__(self, idx: int, name: str, desc: str, kind: str, strVal: str, dateVal: datetime, numVal: float):
        """Constructor."""
        self.idx = idx
        self.name = name
        self.desc = desc
        self.kind = kind
        self.strVal = strVal
        self.dateVal = dateVal
        self.numVal = numVal

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

    def getStrVal(self) -> str:
        """Getter for strVal"""
        return self.strVal

    def setStrVal(self, strVal: str):
        """Setter for strVal"""
        self.strVal = strVal

    def getDateVal(self) -> datetime:
        """Getter for dateVal"""
        return self.dateVal

    def setDateVal(self, dateVal: datetime):
        """Setter for dateVal"""
        self.dateVal = dateVal

    def getNumVal(self) -> float:
        """Getter for numVal"""
        return self.numVal

    def getIntVal(self) -> int:
        """Get numeric value as integer."""
        return int(self.numVal)

    def setNumVal(self, numVal: float):
        """Setter for numVal"""
        self.numVal = numVal

    def toJson(self):
        """Create a dict of this AppParam for json export."""
        data = {
            'idx': self.idx,
            'name': self.name,
            'desc': self.desc,
            'kind': self.kind,
            'strVal': self.strVal,
            'dateVal': self.dateVal,
            'numVal': self.numVal,
        }
        return data

    def __str__(self):
        str = "AppParam"
        str += f' idx: {self.idx}'
        str += f' name: {self.name}'
        str += f' desc: {self.desc}'
        str += f' kind: {self.kind}'
        str += f' strVal: {self.strVal}'
        str += f' dateVal: {self.dateVal}'
        str += f' numVal: {self.numVal}'
        return str


class AppParamCache():
    """Singleton AppParam Cache."""
    log = logging.getLogger("AppParamCache")
    _instance = None

    def __new__(cls):
        """Create a singleton object."""
        if cls._instance is None:
            cls._instance = super(AppParamCache, cls).__new__(cls)
            cls._instance.log.info('Created the AppParamCache singleton')
            cls._instance.load()
        return cls._instance

    def __init__(self):
        """Constructor. Unused as all is done in new."""
        pass

    def getAppParams(self) -> list[AppParam]:
        """Return all objects in cache."""
        return self.appParams

    def load(self):
        """Fetch and store the AppParam records."""
        self.db = Database.Database(config.dbName)
        self.appParams = []
        self.db.connect(config.dbUser, config.dbPass)
        query = Database.Query("AppParam")
        query.add("select idxAppParam, apName, apDesc, apKind, apStrVal, apDateVal, apNumVal from AppParam")
        query.add("order by apName asc")
        rows = self.db.fetch(query.getSQL())
        for row in rows:
            self.appParams.append(AppParam(*row))
        self.db.disconnect()
        query.close()

    def save(self, obj: AppParam):
        """Update the specified AppParam in database."""
        if obj is None:
            self.log.error('Undefined object to save!')
            return
        if obj.getIdx() > 0:
            self.update(obj)
        else:
            self.log.error('Cannot insert AppParam')

    def update(self, obj: AppParam):
        """Update the specified AppParam in database."""
        self.log.info('Updating %s', obj)
        query = Database.Query('Update AppParam')
        query.add('Update AppParam set')
        query.add('apStrVal = ').addEscapedString(obj.getStrVal()).add(',')
        query.add('apDateVal = ').addDate(obj.getDateVal()).add(',')
        query.add(f'apNumVal = {obj.getNumVal()}')
        query.add(f'where idxAppParam = {obj.getIdx()}')
        self.db.connect(config.dbUser, config.dbPass)
        self.db.execute(query.getSQL())
        self.db.disconnect()
        query.close()

    def fetchFromWhere(self, where: str):
        """Fetch AppParam records from a SQL where-clause. Return a list of ids."""
        result = []
        self.db.connect(config.dbUser, config.dbPass)
        query = Database.Query("AppParam")
        query.add('select idxAppParam from AppParam where ' + where)
        rows = self.db.fetch(query.getSQL())
        result = list(row[0] for row in rows)
        query.close()
        self.db.disconnect()
        return result

    def findById(self, idx: int) -> AppParam:
        """Find a AppParam from its primary key."""
        for item in self.getAppParams():
            if item.idx == idx:
                return item
        return None

    def findByName(self, name: str) -> AppParam:
        """Find a AppParam from its unique name."""
        for item in self.getAppParams():
            if item.name == name:
                return item
        return None
    
    def getLastUploadAt(self) -> datetime:
        """Returns the last website upload timestamp."""
        apLastUpload = self.findByName('websiteUpload')
        if apLastUpload:
            return apLastUpload.getDateVal()
        return None

    def __str__(self):
        return 'AppParamCache'

def testAppParamCache():
    """Unit test for AppParamCache"""
    AppParamCache.log.info("Testing AppParamCache")
    cache = AppParamCache()
    for ap in cache.getAppParams():
        cache.log.info(ap)
    apDefLoc = cache.findByName('defLocation')
    cache.log.info('Default location: %d', apDefLoc.getIntVal())
    dtLastUpload = cache.getLastUploadAt()
    cache.log.info(f'last upload: {dtLastUpload}')

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testAppParamCache()

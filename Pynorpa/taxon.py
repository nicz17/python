"""Module for fetching taxa from database."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import config
import Database


class Taxon():
    """Class Taxon"""
    log = logging.getLogger("Taxon")

    def __init__(self, idx: int, name: str, nameFr: str, rank: str, parent: int, order: int, typical: bool):
        """Constructor."""
        self.idx = idx
        self.name = name
        self.nameFr = nameFr
        self.rank = rank
        self.parent = parent
        self.order = order
        self.typical = typical

    def getIdx(self) -> int:
        """Getter for idx"""
        return self.idx

    def getName(self) -> str:
        """Getter for name"""
        return self.name

    def setName(self, name: str):
        """Setter for name"""
        self.name = name

    def getNameFr(self) -> str:
        """Getter for nameFr"""
        return self.nameFr

    def setNameFr(self, nameFr: str):
        """Setter for nameFr"""
        self.nameFr = nameFr

    def getRank(self) -> str:
        """Getter for rank"""
        return self.rank

    def setRank(self, rank: str):
        """Setter for rank"""
        self.rank = rank

    def getParent(self) -> int:
        """Getter for parent"""
        return self.parent

    def setParent(self, parent: int):
        """Setter for parent"""
        self.parent = parent

    def isTopLevel(self) -> bool:
        """Check if this taxon has no parent."""
        return self.parent is None

    def getOrder(self) -> int:
        """Getter for order"""
        return self.order

    def setOrder(self, order: int):
        """Setter for order"""
        self.order = order

    def getTypical(self) -> bool:
        """Getter for typical"""
        return self.typical

    def setTypical(self, typical: bool):
        """Setter for typical"""
        self.typical = typical

    def toJson(self):
        """Create a dict of this Taxon for json export."""
        data = {
            'idx': self.idx,
            'name': self.name,
            'nameFr': self.nameFr,
            'rank': self.rank,
            'parent': self.parent,
            'order': self.order,
            'typical': self.typical,
        }
        return data

    def __str__(self):
        str = "Taxon"
        str += f' idx: {self.idx}'
        str += f' name: {self.name}'
        str += f' nameFr: {self.nameFr}'
        str += f' rank: {self.rank}'
        str += f' parent: {self.parent}'
        str += f' order: {self.order}'
        str += f' typical: {self.typical}'
        return str


class TaxonCache():
    """Class TaxonCache"""
    log = logging.getLogger("TaxonCache")

    def __init__(self):
        """Constructor."""
        self.taxons = []
        self.topLevel = []

    def load(self):
        """Fetch and store the Taxon records from database."""
        db = Database.Database(config.dbName)
        db.connect(config.dbUser, config.dbPass)
        sql = "select idxTaxon, taxName, taxNameFr, taxRank, taxParent, taxOrder, taxTypical from Taxon"
        sql += " order by taxName asc"
        rows = db.fetch(sql)
        for row in rows:
            taxon = Taxon(*row)
            self.taxons.append(taxon)
            if taxon.isTopLevel():
                self.topLevel.append(taxon)
        db.disconnect()
        self.log.info(f'Fetched {len(self.taxons)} taxa from DB')

    def getTopLevelTaxa(self):
        """Get all taxa without parent."""
        return self.topLevel

    def findById(self, idx) -> Taxon:
        """Find a Taxon from its primary key."""
        item: Taxon
        for item in self.taxons:
            if item.idx == idx:
                return item
        return None

    def findByName(self, name) -> Taxon:
        """Find a Taxon from its unique name."""
        item: Taxon
        for item in self.taxons:
            if item.name == name:
                return item
        return None

    def __str__(self):
        str = f'TaxonCache with {len(self.taxons)} taxons'
        return str



def testTaxonCache():
    """Unit test for TaxonCache"""
    TaxonCache.log.info("Testing TaxonCache")
    cache = TaxonCache()
    cache.load()
    tax: Taxon
    for tax in cache.getTopLevelTaxa():
        cache.log.info('Top-level: %s', tax)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testTaxonCache()


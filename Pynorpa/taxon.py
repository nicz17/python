"""Module for fetching taxa from database."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import config
import Database
from enum import Enum


class TaxonRank(Enum):
    """Enum of taxon ranks."""
    KINGDOM  = 0
    PHYLUM   = 1
    CLASS    = 2
    ORDER    = 3
    FAMILY   = 4
    GENUS    = 5
    SPECIES  = 6

    def getNameFr(self):
        name = 'Inconnu'
        match self:
            case TaxonRank.KINGDOM: name = 'Règne'
            case TaxonRank.PHYLUM:  name = 'Phylum'
            case TaxonRank.CLASS:   name = 'Classe'
            case TaxonRank.ORDER:   name = 'Ordre'
            case TaxonRank.FAMILY:  name = 'Famille'
            case TaxonRank.GENUS:   name = 'Genre'
            case TaxonRank.SPECIES: name = 'Espèce'
        return name

    def __str__(self):
        return self.name
    
class Taxon():
    """Class Taxon"""
    log = logging.getLogger("Taxon")

    def __init__(self, idx: int, name: str, nameFr: str, rank: str, parent: int, order: int, typical: bool):
        """Constructor."""
        self.idx = idx
        self.name = name
        self.nameFr = nameFr
        self.rank = TaxonRank[rank]
        self.parent = parent
        self.order = order
        self.typical = typical
        self.children = []

    def addChild(self, child):
        if child is not None:
            self.children.append(child)

    def getChildren(self):
        return self.children

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

    def getRank(self) -> TaxonRank:
        """Getter for rank"""
        return self.rank
    
    def getRankFr(self) -> str:
        """Get translated taxon rank name"""
        return self.rank.getNameFr()

    def setRank(self, rank: TaxonRank):
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
        str += f' rank: {self.rank.name}'
        str += f' parent: {self.parent}'
        str += f' order: {self.order}'
        str += f' typical: {self.typical}'
        return str


class TaxonCache():
    """Class TaxonCache"""
    log = logging.getLogger("TaxonCache")

    def __init__(self):
        """Constructor."""
        self.topLevel = []
        self.dictById = {}

    def load(self):
        """Fetch and store the Taxon records from database."""
        db = Database.Database(config.dbName)
        db.connect(config.dbUser, config.dbPass)
        query = Database.Query('Taxon')
        query.add('select idxTaxon, taxName, taxNameFr, taxRank, taxParent, taxOrder, taxTypical')
        query.add('from Taxon order by taxOrder asc, taxName asc')
        rows = db.fetch(query.getSQL())
        for row in rows:
            taxon = Taxon(*row)
            self.dictById[taxon.getIdx()] = taxon
            if taxon.isTopLevel():
                self.topLevel.append(taxon)
        query.close()
        db.disconnect()
        self.log.info(f'Fetched {len(self.dictById)} taxa from DB')

        # Add children to their parents
        taxon: Taxon
        for taxon in self.dictById.values():
            if taxon.parent is not None:
                parent = self.findById(taxon.parent)
                if parent is not None:
                    parent.addChild(taxon)
                else:
                    self.log.error('Could not find parent of %s', taxon)

    def getTopLevelTaxa(self):
        """Get all taxa without parent."""
        return self.topLevel

    def findById(self, idx: int) -> Taxon:
        """Find a Taxon from its primary key."""
        return self.dictById[idx]

    def findByName(self, name: str) -> Taxon:
        """Find a Taxon from its unique name."""
        item: Taxon
        for item in self.dictById.values():
            if item.name == name:
                return item
        return None

    def __str__(self):
        str = f'TaxonCache with {len(self.dictById)} taxons'
        return str


def testTaxonCache():
    """Unit test for TaxonCache"""
    TaxonCache.log.info("Testing TaxonCache")
    cache = TaxonCache()
    cache.load()
    tax: Taxon
    for tax in cache.getTopLevelTaxa():
        cache.log.info('Top-level: %s', tax)

def testReflection():
    """Simple reflection test"""
    taxon = Taxon(42, 'Test42', 'Bingo', 'NoRank', None, 1, False)
    mtdGetter = Taxon.getNameFr
    result = mtdGetter(taxon)
    taxon.log.info(result)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testTaxonCache()
    testReflection()


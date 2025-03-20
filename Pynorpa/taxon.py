"""Module for fetching taxa from database."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import config
from enum import Enum
import logging

import Database
import TextTools


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

    def getColor(self):
        """Get the hex color code for the taxon."""
        color = '#ffffff'
        if self == TaxonRank.KINGDOM:
            color = '#cf7dff'
        if self == TaxonRank.PHYLUM:
            color = '#8da7ff'
        if self == TaxonRank.CLASS:
            color = '#8dffe6'
        if self == TaxonRank.ORDER:
            color = '#afff8d'
        if self == TaxonRank.FAMILY:
            color = '#ffff8d'
        if self == TaxonRank.GENUS:
            color = '#ffcf8d'
        if self == TaxonRank.SPECIES:
            color = '#ffcdcd'
        return color

    def __str__(self):
        return self.name
    
class Taxon():
    """Class Taxon"""
    log = logging.getLogger("Taxon")

    def __init__(self, idx: int, name: str, nameFr: str, rank: str, idxParent: int, order: int, typical: bool):
        """Constructor."""
        self.idx = idx
        self.name = name
        self.nameFr = nameFr
        self.nameFrNorm = TextTools.replaceAccents(nameFr)
        self.rank = TaxonRank[rank]
        self.idxParent = idxParent
        self.order = order
        self.typical = typical

        self.parent = None
        self.children = []
        self.pictures = []

    def addChild(self, child: 'Taxon'):
        """Add a child of this taxon."""
        if child is not None:
            self.children.append(child)

    def addPicture(self, picture):
        """Add a picture of this taxon."""
        if picture:
            self.pictures.append(picture)

    def getChildren(self) -> list['Taxon']:
        """Get all children of this taxon."""
        return self.children
    
    def getTypicalChild(self) -> 'Taxon':
        """Get the typical child of this taxon, or None."""
        for child in self.getChildren():
            if child.isTypical():
                return child
        if len(self.children) > 0:
            return self.getChildren()[0]
        return None
    
    def getAnyPicture(self):
        """Get any picture of this taxon or its children."""
        if len(self.pictures) > 0:
            return self.pictures[0]
        if len(self.children) > 0:
            return self.getChildren()[0].getAnyPicture()
        return None
    
    def getBestPicture(self):
        """Get the highest quality picture of this taxon."""
        result = None
        maxRating = 0
        for pic in self.pictures:
            if pic.getRating() > maxRating:
                result = pic
                maxRating = pic.getRating()
        return result
    
    def getTypicalPicture(self):
        """Get the most representative picture of this taxon or its children."""
        if len(self.pictures) > 0:
            return self.getBestPicture()
        typicalChild = self.getTypicalChild()
        if typicalChild:
            return typicalChild.getTypicalPicture()
        return None
    
    def getPictures(self) -> list:
        return self.pictures

    def getIdx(self) -> int:
        """Getter for idx"""
        return self.idx

    def getName(self) -> str:
        """Getter for name"""
        return self.name

    def getNameShort(self) -> str:
        """Get shortened name, like A. ursium."""
        if self.rank == TaxonRank.SPECIES:
            (genus, spepi) = self.name.split(' ', maxsplit=1)
            return f'{genus[:1]}. {spepi}'
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

    def getIdxParent(self) -> int:
        """Getter for idxParent"""
        return self.idxParent

    def setParent(self, idxParent: int):
        """Setter for idxParent"""
        self.idxParent = idxParent

    def getParent(self) -> 'Taxon':
        """Getter for parent"""
        return self.parent

    def setParent(self, parent: 'Taxon'):
        """Setter for parent"""
        self.parent = parent

    def getParentName(self) -> str:
        """Returns the parent name, or None."""
        return self.parent.getName() if self.parent else None

    def isTopLevel(self) -> bool:
        """Check if this taxon has no parent."""
        return self.idxParent is None

    def getOrder(self) -> int:
        """Getter for order"""
        return self.order

    def setOrder(self, order: int):
        """Setter for order"""
        self.order = order

    def isTypical(self) -> bool:
        """Check if this taxon is the type of its parent."""
        return self.typical

    def getTypical(self) -> bool:
        """Getter for typical"""
        return self.typical

    def setTypical(self, typical: bool):
        """Setter for typical"""
        self.typical = typical

    def getAncestor(self, rank: TaxonRank) -> 'Taxon':
        """Get our ancestor at the specified rank."""
        if self.rank == rank:
            return self
        elif self.parent:
            return self.getParent().getAncestor(rank)
        return None

    def toJson(self):
        """Create a dict of this Taxon for json export."""
        data = {
            'idx': self.idx,
            'name': self.name,
            'nameFr': self.nameFr,
            'rank': self.rank,
            'idxParent': self.idxParent,
            'order': self.order,
            'typical': self.typical,
        }
        return data

    def __str__(self):
        str = f'Taxon {self.idx} {self.name} -- {self.nameFr} {self.rank.name}'
        str += f' idxParent: {self.idxParent} order: {self.order} typical: {self.typical}'
        return str


class TaxonCache():
    """Singleton class to fetch Taxon records from database and cache them."""
    log = logging.getLogger("TaxonCache")
    _instance = None

    def __new__(cls):
        """Create a singleton object."""
        if cls._instance is None:
            cls._instance = super(TaxonCache, cls).__new__(cls)
            cls._instance.log.info('Created the TaxonCache singleton')
            cls._instance.load()
        return cls._instance

    def __init__(self):
        """Constructor. Unused as all is done in new."""
        pass

    def load(self):
        """Fetch and store the Taxon records from database."""
        self.db = Database.Database(config.dbName)
        self.topLevel = []
        self.dictById = {}
        self.db.connect(config.dbUser, config.dbPass)
        query = Database.Query('Taxon')
        query.add('select idxTaxon, taxName, taxNameFr, taxRank, taxParent, taxOrder, taxTypical')
        query.add('from Taxon order by taxOrder asc, taxName asc')
        rows = self.db.fetch(query.getSQL())
        for row in rows:
            taxon = Taxon(*row)
            self.dictById[taxon.getIdx()] = taxon
            if taxon.isTopLevel():
                self.topLevel.append(taxon)
        query.close()
        self.db.disconnect()
        self.log.info(f'Fetched {len(self.dictById)} taxa from DB')

        # Add children to their parents
        taxon: Taxon
        for taxon in self.dictById.values():
            if taxon.idxParent is not None:
                parent = self.findById(taxon.idxParent)
                if parent is not None:
                    parent.addChild(taxon)
                    taxon.setParent(parent)
                else:
                    self.log.error('Could not find parent of %s', taxon)

    def save(self, obj: Taxon):
        """Insert or update the specified Taxon in database."""
        if obj is None:
            self.log.error('Undefined object to save!')
            return
        if obj.getIdx() > 0:
            self.update(obj)
        else:
            self.insert(obj)

    def update(self, obj: Taxon):
        """Update the specified Taxon in database."""
        self.log.info('Updating %s', obj)
        query = Database.Query('Update Taxon')
        query.add('Update Taxon set')
        query.add('taxName = ').addEscapedString(obj.getName()).add(',')
        query.add('taxNameFr = ').addEscapedString(obj.getNameFr()).add(',')
        #query.add('taxRank = ').addEscapedString(obj.getRank().name).add(',')
        query.add(f'taxParent = {obj.getIdxParent()},')
        query.add(f'taxOrder = {obj.getOrder()},')
        query.add('taxTypical = ').addBool(obj.getTypical())
        query.add(f'where idxTaxon = {obj.getIdx()}')
        self.db.connect(config.dbUser, config.dbPass)
        self.db.execute(query.getSQL())
        self.db.disconnect()
        query.close()

    def insert(self, obj: Taxon):
        """Insert the specified Taxon in database."""
        self.log.info('Inserting %s', obj)
        query = Database.Query('Insert Taxon')
        query.add('Insert into Taxon (idxTaxon, taxName, taxNameFr, taxRank, taxParent, taxOrder, taxTypical)')
        query.add('values (null')
        query.add(',').addEscapedString(obj.getName())
        query.add(',').addEscapedString(obj.getNameFr())
        query.add(',').addEscapedString(obj.getRank().name)
        query.add(',').addNullableFK(obj.getIdxParent())
        query.add(f', {obj.getOrder()}')
        query.add(',').addBool(obj.getTypical())
        query.add(')')
        self.db.connect(config.dbUser, config.dbPass)
        idx = self.db.execute(query.getSQL())
        self.db.disconnect()
        query.close()
        if idx:
            self.log.info(f'Inserted with idx {idx}')
            obj.idx = idx
            self.dictById[obj.getIdx()] = obj
        else:
            self.log.error('No idx after insertion!')

    def fetchFromWhere(self, where: str) -> list[int]:
        """Fetch Taxon records from a SQL where-clause. Return a list of ids."""
        self.log.info(f'Fetching from Taxon where {where}')
        self.db.connect(config.dbUser, config.dbPass)
        query = Database.Query('Taxon')
        query.add(f'select idxTaxon from Taxon where {where}')
        query.add('order by taxOrder asc, taxName asc')
        rows = self.db.fetch(query.getSQL())
        result = list(row[0] for row in rows)
        query.close()
        self.db.disconnect()
        self.log.info(f'Fetched {len(result)} taxa from DB where {where}')
        return result
    
    def fetchNewestSpecies(self, limit=8):
        """Fetch the most recently discovered species."""
        self.db.connect(config.dbUser, config.dbPass)
        query = Database.Query('Newest species')
        query.add('select idxTaxon,')
        query.add('(select min(picShotAt) from Picture where picTaxon = idxTaxon) as tFirstObs')
        query.add("from Taxon where taxRank = 'SPECIES'")
        query.add(f'order by tFirstObs desc limit {limit}')
        result = self.db.fetch(query.getSQL())
        query.close()
        self.db.disconnect()
        return result

    def getTopLevelTaxa(self) -> list[Taxon]:
        """Get all taxa without parent."""
        return self.topLevel
    
    def getForRank(self, rank: TaxonRank) -> list[Taxon]:
        """Get all taxa of the specified rank."""
        result = []
        for taxon in self.dictById.values():
            if taxon.rank == rank:
                result.append(taxon)
        return result

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

    def findByFilename(self, filename: str) -> Taxon:
        """Find a Taxon from a file name."""
        name = filename.removesuffix('.jpg')
        name = TextTools.removeDigits(name)
        name = TextTools.upperCaseFirst(name)
        name = name.replace('-sp', '')
        name = name.replace('-', ' ')
        return self.findByName(name)
    
    def createTaxonForFilename(self, filename: str, dryrun=False) -> Taxon:
        """Create a Taxon from a file name and save to DB."""
        self.log.info('Will create a taxon for filename %s', filename)

        # Extract taxon name from filename
        name = filename.removesuffix('.jpg')
        name = TextTools.removeDigits(name)
        name = TextTools.upperCaseFirst(name)
        rank = TaxonRank.SPECIES
        if name.endswith('-sp'):
            name = name.removesuffix('-sp')
            rank = TaxonRank.GENUS
        elif name.endswith('idae') or name.endswith('aceae'):
            rank = TaxonRank.FAMILY
        name = name.replace('-', ' ')

        # If species, also find or create Genus
        parent = None
        if rank == TaxonRank.SPECIES:
            nameGenus = name.split()[0]
            parent = self.findByName(nameGenus)
            if parent:
                if parent.rank != TaxonRank.GENUS:
                    self.log.error('Wrong rank for parent %s, expected Genus', parent)
                else:
                    self.log.info('Using existing Genus %s as parent', parent)
            else:
                self.log.info('Creating Genus %s as parent', nameGenus)
                parent = self.createTaxonForFilename(nameGenus + '-sp', dryrun)

        # Create taxon and save to DB unless dry-run
        # TODO: find or create parents all the way up
        idxParent = parent.getIdx() if parent else -1
        taxon = Taxon(-1, name, name, rank.name, idxParent, 0, False)
        taxon.setParent(parent)
        if not dryrun:
            self.insert(taxon)
        self.log.info('Created taxon %s', taxon)
        return taxon
    
    def createChildTaxon(self, parent: Taxon):
        """Create a child of the specified taxon and return it unsaved."""
        rank = TaxonRank(parent.rank.value+1)
        name = None
        nameFr = None
        if parent.rank == TaxonRank.GENUS:
            name   = parent.name
            nameFr = parent.nameFr
        child = Taxon(-1, name, nameFr, rank.name, parent.idx, 0, False)
        child.setParent(parent)
        return child
        
    def __str__(self):
        return f'TaxonCache with {len(self.dictById)} taxa'


def testTaxonCache():
    """Unit test for TaxonCache"""
    TaxonCache.log.info("Testing TaxonCache")
    cache = TaxonCache()
    tax: Taxon
    for tax in cache.getTopLevelTaxa():
        cache.log.info('Top-level: %s', tax)
    #where = "taxName like '%anth%pe%'"
    #ids = cache.fetchFromWhere(where)
    # for idx in ids:
    #     taxon = cache.findById(idx)
    #     if taxon:
    #         cache.log.info(taxon)
    rows = cache.fetchNewestSpecies()
    for (idx, tFirstObs) in rows:
        taxon = cache.findById(idx)
        if taxon:
            cache.log.info('%s first observed %s', taxon, tFirstObs)
    
    filename = 'anas-clypeata008.jpg'
    taxon = cache.findByFilename(filename)
    cache.log.info('File %s taxon %s', filename, taxon)

def testCreateTaxaFromFilename():
    """Unit test for creating a species and its genus from a file name."""
    cache = TaxonCache()
    cache.log.info('Testing creation of taxa from filenames')
    cache.createTaxonForFilename('blastus-vulgaris001.jpg', True)
    cache.createTaxonForFilename('anas-fantasticus001.jpg', True)
    cache.createTaxonForFilename('blastidae4242.jpg', True)

def testReflection():
    """Simple reflection test"""
    TaxonCache.log.info("Testing reflection")
    taxon = Taxon(42, 'Test42', 'Bingo', 'FAMILY', None, 1, False)
    mtdGetter = Taxon.getNameFr
    result = mtdGetter(taxon)
    taxon.log.info(result)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testTaxonCache()
    testCreateTaxaFromFilename()
    #testReflection()


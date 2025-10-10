"""Module bookManager"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import config
import glob
import json
import logging
import os

import DateTools
from taxon import Taxon, TaxonCache
from LocationCache import Location, LocationCache
from picture import Picture, PictureCache
from Database import Query
from PhotoInfo import PhotoInfo
from pynorpaHtml import PynorpaHtmlPage
from HtmlPage import *

class BookPicFilter():
    """Class BookPicFilter"""
    log = logging.getLogger("BookPicFilter")

    def __init__(self):
        """Constructor."""
        self.locCache = LocationCache()
        self.taxon = None
        self.location = self.locCache.getDefaultLocation()
        self.quality = 4

    def getFilterClause(self) -> Query:
        """Build the filtering SQL."""
        query = Query('BookPicFilter')
        query.add('1=1')
        if self.quality > 1:
            query.add(f'and picRating >= {self.quality}')
        if self.location:
            query.add(f'and picIdxLocation = {self.location.getIdx()}')
        # TODO handle taxon clause
        query.add('order by picFilename asc')
        return query

    def getTaxon(self) -> Taxon:
        """Getter for taxon"""
        return self.taxon

    def setTaxon(self, taxon: Taxon):
        """Setter for taxon"""
        self.taxon = taxon

    def getLocation(self) -> Location:
        """Getter for location"""
        return self.location

    def getLocationName(self) -> str:
        """Getter for location name"""
        if self.location:
            return self.location.getName()
        return 'Tous'

    def setLocation(self, location: Location):
        """Setter for location"""
        self.location = location

    def getQuality(self) -> int:
        """Getter for quality"""
        return self.quality

    def setQuality(self, quality: int):
        """Setter for quality"""
        self.quality = quality

    def toJson(self):
        """Create a dict of this filter for json export."""
        data = {
            'idxTaxon': self.taxon.idx if self.taxon else None, 
            'idxLocation': self.location.idx if self.location else None,
            'quality': self.quality
        }
        return data

    def __str__(self):
        str = "BookPicFilter"
        str += f' taxon: {self.taxon}'
        str += f' location: {self.location}'
        str += f' quality: {self.quality}'
        return str


class PictureInBook(Picture):
    """Subclass of Picture for books."""
    log = logging.getLogger("PictureInBook")

    def __init__(self, pic: Picture, book: 'Book', caption: str, order: int):
        """Constructor."""
        super().__init__(pic.idx, pic.filename, pic.shotAt, pic.remarks, pic.idxTaxon,
                         pic.updatedAt, pic.idxLocation, pic.rating)
        self.book = book
        self.caption = caption
        self.order = order
        self.orig = None

    def getCaption(self) -> str:
        """Getter for caption"""
        return self.caption

    def setCaption(self, caption: str):
        """Setter for caption"""
        self.caption = caption

    def getOrder(self) -> int:
        """Getter for order"""
        return self.order

    def setOrder(self, order: int):
        """Setter for order"""
        self.order = order

    def hasOriginal(self) -> bool:
        """Checks if the original photo exists in book dir."""
        return os.path.exists(self.getOrigFilename())

    def getOrigSize(self) -> str:
        """Get size of original image, or - if no original."""
        if self.hasOriginal():
            info = PhotoInfo(self.getOrigFilename())
            info.identify()
            return info.getSizeString()
        return '-'
    
    def getOrigFilename(self) -> str:
        """Get original photo filename in book dir."""
        return f'{self.book.getBookDir()}/orig/{self.filename}'

    def toJson(self):
        """Create a dict of this PictureInBook for json export."""
        data = {
            'idx': self.idx,
            'filename': self.filename,
            'caption': self.caption,
            'order': self.order,
            'orig': self.orig
        }
        return data

    def __str__(self):
        return f'PictureInBook {self.filename} order {self.order}'
    

class Book():
    """A printed picture book."""
    log = logging.getLogger("Book")

    def __init__(self, name: str, desc: str):
        """Constructor."""
        self.name = name
        self.desc = desc
        self.status = 'Projet'
        self.filter = None
        self.pictures = []

    def getName(self) -> str:
        """Getter for name"""
        return self.name
    
    def setName(self, name: str):
        self.name = name
    
    def getDesc(self) -> str:
        """Getter for desc"""
        return self.desc
    
    def setDesc(self, desc: str):
        self.desc = desc

    def getStatus(self) -> str:
        """Getter for status"""
        return self.status
    
    def setStatus(self, status: str):
        self.status = status

    def getFilter(self) -> BookPicFilter:
        return self.filter
    
    def setFilter(self, filter: BookPicFilter):
        self.filter = filter

    def addPicture(self, pic: PictureInBook):
        """Add picture."""
        self.pictures.append(pic)

    def getPictures(self) -> list[PictureInBook]:
        """Getter for pictures"""
        return self.pictures
    
    def getPicCount(self) -> int:
        """Count the pictures in this book."""
        return len(self.pictures)
    
    def getBookDir(self) -> str:
        """Get the book directory."""
        return f'{config.dirBooks}{self.getName()}'

    def toJson(self):
        """Create a dict of this Book for json export."""
        pics = []
        for pic in self.getPictures():
            pics.append(pic.toJson())
        data = {
            'name': self.name,
            'desc': self.desc,
            'status': self.status,
            'filter': self.filter.toJson(),
            'pictures': pics
        }
        return data

    def __str__(self):
        return f'Book {self.name} [{self.status}] {self.desc}'


class BookManager():
    """Class BookManager"""
    log = logging.getLogger("BookManager")

    def __init__(self):
        """Constructor."""
        self.books = []
        self.picCache = PictureCache()
        self.locCache = LocationCache()
        self.taxCache = TaxonCache()

    def addBook(self) -> Book:
        """Add a new book and return it."""
        name = f'Livre{len(self.books)+1}'
        book = Book(name, 'Nouveau livre')
        book.setFilter(BookPicFilter())
        self.books.append(book)
        return book

    def getBooks(self) -> list[Book]:
        """Get all loaded books."""
        return self.books

    def loadBooks(self):
        """Load books from disk."""
        self.log.info('Loading books')
        dirs = sorted(glob.glob(config.dirBooks + '*'))
        for dir in dirs:
            if os.path.isdir(dir):
                filename = f'{dir}/book.json'
                if os.path.exists(filename):
                    book = self.loadBook(filename)
                    self.books.append(book)
                    self.log.info(book)
        self.log.info(f'Loaded {len(self.books)} books')

    def loadBook(self, filename: str) -> Book:
        """Load a book from its json file."""
        book = None
        with open(filename, 'r') as file:
            data = json.load(file)
            book = Book(data['name'], data['desc'])
            book.status = data['status']
            for pibData in data['pictures']:
                book.addPicture(self.loadPicture(pibData, book))
            filter = data['filter']
            book.setFilter(self.loadFilter(filter['idxLocation'], filter['idxTaxon'], filter['quality']))
        return book
    
    def loadPicture(self, data, book: Book) -> PictureInBook:
        """Create a PictureInBook from json data."""
        pic = self.picCache.findById(data['idx'])
        pib = PictureInBook(pic, book, data['caption'], data['order'])
        if 'orig' in data:
            pib.orig = data['orig']
        return pib
    
    def loadFilter(self, idxLocation: int, idxTaxon: int, quality: int) -> BookPicFilter:
        """Create a filter from json data."""
        filter = BookPicFilter()
        filter.setLocation(None if idxLocation is None else self.locCache.getById(idxLocation))
        filter.setTaxon(None if idxTaxon is None else self.taxCache.findById(idxTaxon))
        filter.setQuality(quality)
        return filter
        
    def saveBook(self, book: Book):
        """Save the book to json."""
        self.log.info(f'Saving {book}')

        # Create directories if needed
        dir = self.getBookDir(book)
        if not os.path.exists(dir):
            self.log.info(f'Creating dir {dir}')
            os.mkdir(dir)
            os.mkdir(f'{dir}/orig')
            os.mkdir(f'{dir}/photos')
            os.mkdir(f'{dir}/medium')
            os.mkdir(f'{dir}/html')

        # Save book as json
        filename = f'{dir}/book.json'
        self.log.info(f'Writing {filename}')
        with open(filename, 'w') as file:
            file.write(json.dumps(book.toJson(), indent=2))

    def addPictureInBook(self, pic: Picture, book: Book) -> PictureInBook:
        """Add a picture to a book and return it."""
        pib = PictureInBook(pic, book, self.buildCaption(pic, book), book.getPicCount()+1)
        self.log.info(f'Adding {pib} to {book}')
        book.addPicture(pib)
        orig = self.findOriginal(pic)
        if orig:
            pib.orig = orig.getNameFull()
        self.saveBook(book)

        # Copy photos to book dir
        dir = self.getBookDir(book)
        self.runSystemCommand(f'cp {config.dirPictures}{pic.filename} {dir}/photos/{pic.filename}')
        if orig:
            self.runSystemCommand(f'cp {orig.filename} {dir}/orig/{pic.filename}')
        return pib

    def buildCaption(self, pic: Picture, book: Book) -> str:
        """Get the caption for the picture."""
        sTaxon = pic.getTaxonName()
        if pic.taxon.getNameFr() != pic.getTaxonName():
            sTaxon = f'{pic.taxon.getNameFr()} ({pic.getTaxonName()})'
        sLoc = '' if book.getFilter().getLocation() else f', {pic.getLocationName()}'
        sShotAt = DateTools.datetimeToPrettyStringFr(pic.getShotAt())
        sRemarks = f'. {pic.getRemarks()}' if pic.getRemarks() else ''
        caption = f'{sTaxon}{sLoc}, {sShotAt}{sRemarks}'
        return caption
    
    def getBookDir(self, book: Book) -> str:
        """Get the book directory."""
        return book.getBookDir()
    
    def createMediumImages(self, book: Book):
        """Convert book photos to medium size."""
        dir = self.getBookDir(book)
        for pib in book.getPictures():
            self.runSystemCommand(f'convert {dir}/photos/{pib.filename} -resize 500x500 {dir}/medium/{pib.filename}')

    def toHtml(self, book: Book):
        """Export a book as html preview."""
        self.log.info(f'Exporting {book} to html')
        self.createMediumImages(book)

        # Create html page
        page = PynorpaHtmlPage(book.getDesc())
        page.addHeading(1, book.getDesc())
        for pib in book.getPictures():
            page.addHeading(3, f'Photo {pib.getOrder()}')
            page.addTag(ImageHtmlTag(f'../medium/{pib.filename}', pib.getCaption()))
            page.addTag(HtmlTag('p', pib.getCaption()))

        # Save page and open in browser
        filename = f'{self.getBookDir(book)}/html/book.html'
        page.save(filename)
        self.runSystemCommand(f'firefox {filename}')

    def findOriginal(self, pic: Picture) -> PhotoInfo:
        """Find original picture. Look in disk in backups."""
        self.log.info(f'Looking for original of {pic}')
        paths = [config.dirPhotosBase, config.dirElements + 'Pictures/']
        yearMonth = DateTools.datetimeToString(pic.getShotAt(), '%Y-%m')
        picShotAt = pic.getShotAt().timestamp()
        for path in paths:
            dir = f'{path}Nature-{yearMonth}/orig/'
            self.log.info(f'Looking in {dir}')
            if os.path.exists(dir):
                files = sorted(glob.glob(f'{dir}*.JPG'))
                self.log.info(f'Scanning {len(files)} files...')
                for file in files:
                    info = PhotoInfo(file)
                    info.identify()
                    if info.getShotAt() == picShotAt:
                        self.log.info(f'Found original: {info}')
                        return info
            else:
                self.log.info(f'Path does not exist: {dir}')
        self.log.info(f'Could not find original of {pic}')
    
    def runSystemCommand(self, cmd: str, dryrun=False):
        """Run a system command."""
        if dryrun:
            self.log.info('dryrun: %s', cmd)
        else:
            os.system(cmd)

    def __str__(self):
        return 'BookManager'


def testBookManager():
    """Unit test for BookManager"""
    BookManager.log.info("Testing BookManager")
    mgr = BookManager()
    mgr.loadBooks()
    book = Book('Test01', 'Test Book 1')

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testBookManager()

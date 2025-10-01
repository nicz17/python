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
from taxon import Taxon
from LocationCache import Location, LocationCache
from picture import Picture
from Database import Query
from PhotoInfo import PhotoInfo


class Book():
    """A printed picture book."""
    log = logging.getLogger("Book")

    def __init__(self, name: str, desc: str):
        """Constructor."""
        self.name = name
        self.desc = desc
        self.status = 'Projet'
        self.pictures = []

    def getName(self) -> str:
        """Getter for name"""
        return self.name

    def getDesc(self) -> str:
        """Getter for desc"""
        return self.desc

    def getStatus(self) -> str:
        """Getter for status"""
        return self.status

    def addPicture(self, pic: Picture):
        """Add picture."""
        self.pictures.append(pic)

    def getPictures(self) -> list[Picture]:
        """Getter for pictures"""
        return self.pictures
    
    def getPicCount(self) -> int:
        """Count the pictures in this book."""
        return len(self.pictures)

    def toJson(self):
        """Create a dict of this Book for json export."""
        pics = []
        for pic in self.getPictures():
            pics.append({
                'id': pic.getIdx(),
                'filename': pic.getFilename()
            })
        data = {
            'name': self.name,
            'desc': self.desc,
            'status': self.status,
            'pictures': pics
        }
        return data

    def __str__(self):
        return f'Book {self.name} {self.status}'


class BookManager():
    """Class BookManager"""
    log = logging.getLogger("BookManager")

    def __init__(self):
        self.books = []

    def addBook(self):
        """Add book."""
        # TODO: implement addBook
        pass

    def getBooks(self) -> list[Book]:
        return self.books

    def loadBooks(self):
        """Load books."""
        # TODO: implement loadBooks
        pass
        
    def saveBook(self, book: Book):
        """Save the book to json."""
        self.log.info(f'Saving {book}')

        # Create dir if needed
        dir = f'{config.dirBooks}{book.getName()}'
        if not os.path.exists(dir):
            self.log.info(f'Creating dir {dir}')
            os.mkdir(dir)
            os.mkdir(f'{dir}/photos')
            os.mkdir(f'{dir}/medium')

        # Save book as json
        filename = f'{dir}/book.json'
        self.log.info(f'Writing {filename}')
        with open(filename, 'w') as file:
            file.write(json.dumps(book.toJson(), indent=2))

    def toHtml(self, book: Book):
        """Export a book as html preview."""
        # TODO: implement toHtml
        pass

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

    def __str__(self):
        return 'BookManager'


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

    def __str__(self):
        str = "BookPicFilter"
        str += f' taxon: {self.taxon}'
        str += f' location: {self.location}'
        str += f' quality: {self.quality}'
        return str


def testBook():
    """Unit test for Book"""
    Book.log.info("Testing Book")
    book = Book("nameExample", "descExample")
    book.log.info(book)
    book.getName()
    book.getDesc()
    book.getStatus()
    book.getPictures()
    book.save()
    book.log.info(book.toJson())

def testBookManager():
    """Unit test for BookManager"""
    BookManager.log.info("Testing BookManager")
    mgr = BookManager()
    mgr.loadBooks()
    book = Book('Test01', 'Test Book 1')
    mgr.saveBook(book)

def testBookPicFilter():
    """Unit test for BookPicFilter"""
    BookPicFilter.log.info("Testing BookPicFilter")
    book = BookPicFilter()
    book.log.info(book)
    book.getTaxon()
    book.getLocation()
    book.getQuality()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    #testBook()
    testBookManager()
    #testBookPicFilter()

"""Module bookManager"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import logging

from taxon import Taxon
from LocationCache import Location, LocationCache
from picture import Picture
from Database import Query


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

    def getPictures(self) -> list:
        """Getter for pictures"""
        return self.pictures

    def save(self):
        """Save."""
        # TODO: implement save
        pass

    def toJson(self):
        """Create a dict of this Book for json export."""
        data = {
            'name': self.name,
            'desc': self.desc,
            'status': self.status,
            'pictures': self.pictures
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

    def saveBooks(self):
        """Save books."""
        # TODO: implement saveBooks
        pass

    def toHtml(self, book: Book):
        """Export a book as html preview."""
        # TODO: implement toHtml
        pass

    def findOriginal(self, pic: Picture):
        """Find original picture."""
        # TODO: implement findOriginal
        pass

    def toJson(self):
        """Create a dict of this BookManager for json export."""
        data = {
            'books': self.books,
        }
        return data

    def __str__(self):
        str = "BookManager"
        str += f' books: {self.books}'
        return str


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

def testBookPicFilter():
    """Unit test for BookPicFilter"""
    BookPicFilter.log.info("Testing BookPicFilter")
    book = BookPicFilter()
    book.log.info(book)
    book.BookPicFilter()
    book.getTaxon()
    book.getLocation()
    book.getQuality()
    book.log.info(book.toJson())

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testBook()
    testBookManager()
    testBookPicFilter()

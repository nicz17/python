"""
Module for the Pynorpa journal.
The journal groups pictures by date and location.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import logging
from datetime import datetime

import DateTools
from picture import Picture, PictureCache
from LocationCache import Location


class JournalItem():
    """A Journal item."""
    log = logging.getLogger('JournalItem')

    def __init__(self, dtAt: datetime, loc: Location):
        """Constructor."""
        self.dtAt = dtAt
        self.location = loc
        self.pics = []

    def addPicture(self, pic: Picture):
        """Adds a picture to this journal item."""
        self.pics.append(pic)

    def size(self) -> int:
        """Count the pictures in this journal item."""
        return len(self.pics)
    
    def __str__(self):
        sAt = DateTools.datetimeToString(self.dtAt, '%Y.%m.%d')
        return f'JournalItem {sAt}  {self.size()} pics  {self.location.getName()}'

class Journal():
    """Class to build the Journal."""
    log = logging.getLogger('Journal')

    def __init__(self, dtFrom: datetime, dtTo: datetime):
        """Constructor."""
        self.dictItems = {}
        self.picCache = PictureCache()

        # Fetch pictures in date-range
        pics = self.picCache.getForJournal(dtFrom, dtTo)
        self.log.info('Fetched %d pictures', len(pics))

        # Group pictures by date and location
        for pic in pics:
            self.log.debug(pic)
            item = None
            loc = pic.getLocation()
            dtDay = DateTools.datetimeToMidnight(pic.getShotAt())
            if dtDay in self.dictItems:
                if loc.getIdx() in self.dictItems[dtDay]:
                    item = self.dictItems[dtDay][loc.getIdx()]
            else:
                self.dictItems[dtDay] = {}
            if item is None:
                item = JournalItem(dtDay, loc)
                self.dictItems[dtDay][loc.getIdx()] = item
            item.addPicture(pic)

        # Dump results
        for dtDay in self.dictItems.keys():
            for idxLoc in self.dictItems[dtDay].keys():
                item = self.dictItems[dtDay][idxLoc]
                self.log.info(item)


def testJournal():
    dtFrom = datetime(2025, 1, 1)
    journal = Journal(dtFrom, None)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testJournal()
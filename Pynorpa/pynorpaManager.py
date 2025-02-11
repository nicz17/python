"""Module for the Pynorpa manager."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
import os

import DateTools
from LocationCache import Location
from PhotoInfo import PhotoInfo
from picture import Picture, PictureCache
from taxon import TaxonCache

class PynorpaManager():
    """Singleton class to manage Pynorpa."""
    log = logging.getLogger('PynorpaManager')
    _instance = None

    def __new__(cls):
        """Create a singleton object."""
        if cls._instance is None:
            cls._instance = super(PynorpaManager, cls).__new__(cls)
            cls._instance.log.info('Created the PynorpaManager singleton')
            cls._instance.init()
        return cls._instance

    def __init__(self):
        """Constructor. Unused as this is a singleton."""
        pass

    def init(self):
        """Initialize members."""
        self.taxonCache = TaxonCache()
        self.pictureCache = PictureCache()

    def addPicture(self, filename: str, loc: Location) -> Picture:
        """Add a new Picture to gallery."""
        self.log.info('Adding picture %s at %s', filename, loc)
        # Check picture is not added yet
        basename = os.path.basename(filename)
        pic = self.pictureCache.findByName(basename)
        if pic:
            self.log.error('Picture is already in gallery: %s', pic)
            return None
        info = PhotoInfo(filename)
        info.identify()
        tShotAt = DateTools.timestampToDatetimeUTC(info.getShotAt())
        taxon = self.taxonCache.findByFilename(basename)
        if taxon:
            pic = Picture(-1, basename, tShotAt, None, taxon.getIdx(), DateTools.nowDatetime(), loc.getIdx(), 3)
            pic.taxon = taxon
            pic.location = loc
            self.log.info('Will add %s', pic)
            return pic
        else:
            self.log.error('Failed to find taxon for %s', filename)
            # TODO GUI error dialog
            return None
        
def testManager():
    """Unit test for manager"""
    mgr = PynorpaManager()
    mgr.log.info('Testing PynorpaManager')
    mgr.addPicture('vanessa-cardui004.jpg', None)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testManager()
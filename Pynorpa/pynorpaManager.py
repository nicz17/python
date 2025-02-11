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
from picture import Picture
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

    def addPicture(self, filename: str, loc: Location) -> Picture:
        """Add a new Picture to gallery."""
        self.log.info('Adding picture %s at %s', filename, loc)
        # TODO check picture is not added yet
        info = PhotoInfo(filename)
        info.identify()
        tShotAt = DateTools.timestampToDatetimeUTC(info.getShotAt())
        taxon = self.taxonCache.findByFilename(os.path.basename(filename))
        if taxon:
            pic = Picture(-1, filename, tShotAt, None, taxon.getIdx(), DateTools.nowDatetime(), loc.getIdx(), 3)
            pic.taxon = taxon
            pic.location = loc
            self.log.info('Will add %s', pic)
            return pic
        else:
            self.log.error('Failed to find taxon for %s', filename)
            # TODO GUI error dialog
            return None
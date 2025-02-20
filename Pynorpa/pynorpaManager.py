"""Module for the Pynorpa manager."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
import os

import DateTools
import TextTools
from GeoTracker import GeoTrack
from LocationCache import Location
from PhotoInfo import PhotoInfo
from picture import Picture, PictureCache
from taxon import TaxonCache


class PynorpaException(Exception):
    """Subclass of Exception for Pynorpa error handling."""
    pass

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

        # Check file exists
        if not os.path.exists(filename):
            raise PynorpaException(f"La photo n'existe pas : {filename}")
        
        # Check location
        if not loc or loc.getIdx() < 1:
            raise PynorpaException(f"Lieu invalide : {loc}")
        # TODO compare with GPS data if defined

        # Check picture is not added yet
        basename = os.path.basename(filename)
        pic = self.pictureCache.findByName(basename)
        if pic:
            self.log.error('Picture is already in gallery: %s', pic)
            msg = f'{pic.getFilename()}\n{pic.getLocationName()}\n{pic.getShotAt()}'
            raise PynorpaException(f'La photo est déjà en galerie :\n{msg}')
        # TODO check file is not yet in config.dirPictures
        
        # Check image size
        info = PhotoInfo(filename)
        info.identify()
        if info.width > 2000 or info.height > 2000:
            raise PynorpaException(f'Taille invalide : {info.getSizeString()}')

        # Check taxon can be found from file name
        taxon = self.taxonCache.findByFilename(basename)
        if not taxon:
            self.log.error('Failed to find taxon for %s', filename)
            raise PynorpaException(f"Taxon inconnu pour {basename}")
        
        # Create Picture
        tShotAt = DateTools.timestampToDatetimeUTC(info.getShotAt())
        rating = 3
        if info.width < 1000 or info.height < 1000:
            rating = 2
        pic = Picture(-1, basename, tShotAt, None, taxon.getIdx(), DateTools.nowDatetime(), loc.getIdx(), rating)
        pic.taxon = taxon
        pic.location = loc
        self.log.info('Will add %s', pic)

        # TODO copy files to gallery

        return pic
            
    def addLocation(self, filename: str) -> Location:
        """Add a location from a GeoTrack file."""
        self.log.info('Adding location from %s', filename)

        # Check file exists
        if not os.path.exists(filename):
            raise PynorpaException(f"Le GeoTrack n'existe pas : {filename}")
        
        # Load track
        track = GeoTrack(filename)
        track.loadData()

        # Create Location
        name = TextTools.removeDigits(track.name)
        loc = Location(-1, name, name, track.center.latitude, track.center.longitude, 
                       track.center.elevation, 'Vaud', 16, 'Suisse')
        self.log.info('Adding %s', loc)
        return loc

        
def testManager():
    """Unit test for manager"""
    mgr = PynorpaManager()
    mgr.log.info('Testing PynorpaManager')
    mgr.addLocation(config.dirSourceGeoTrack + 'Lauenensee250216.gpx')
    mgr.addPicture('vanessa-cardui004.jpg', None)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testManager()
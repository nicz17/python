"""Module for the Pynorpa manager."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
import os
from tkinter import messagebox as mb

import DateTools
import TextTools
from GeoTracker import GeoTrack
from LocationCache import Location, LocationCache
from PhotoInfo import PhotoInfo
from picture import Picture, PictureCache
from taxon import TaxonCache
from expedition import Expedition, ExpeditionCache


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
        self.locationCache = LocationCache()
        self.expeditionCache = ExpeditionCache()

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
            self.log.error('Picture is already in DB: %s', pic)
            msg = f'{pic.getFilename()}\n{pic.getLocationName()}\n{pic.getShotAt()}'
            raise PynorpaException(f'La photo est déjà dans la base :\n{msg}')
        # Check file is not yet in config.dirPictures
        dest = f'{config.dirPictures}{basename}'
        if os.path.exists(dest):
            self.log.error('Picture is already on disk: %s', dest)
            raise PynorpaException(f'La photo est déjà sur le disque')
        
        # Check image size
        info = PhotoInfo(filename)
        info.identify()
        if info.width > 2000 or info.height > 2000:
            self.log.error('Invalid photo size %s', info.getSizeString())
            raise PynorpaException(f'Taille invalide : {info.getSizeString()}')

        # Check taxon can be found from file name
        taxon = self.taxonCache.findByFilename(basename)
        if not taxon:
            self.log.error('Failed to find taxon for %s', filename)
            reply = mb.askquestion('Taxon inconnu', f'Créer des taxons pour {basename} ?')
            if reply == 'yes':
                self.log.info('Will create taxa for %s', basename)
                taxon = self.taxonCache.createTaxonForFilename(basename)
                if taxon:
                    self.log.info('Created %s', taxon)
                    if taxon.getIdx() < 1:
                        raise PynorpaException(f"Taxon invalide pour {basename}")
                else:
                    raise PynorpaException(f'Echec de création de taxon pour {basename}')
            else:
                raise PynorpaException(f"Taxon inconnu pour {basename}")
        
        # Create Picture
        tShotAt = DateTools.timestampToDatetimeUTC(info.getShotAt())
        rating = 3
        if info.width < 1000 or info.height < 1000:
            rating = 2
        pic = Picture(-1, basename, tShotAt, None, taxon.getIdx(), DateTools.nowDatetime(), loc.getIdx(), rating)
        pic.taxon = taxon
        pic.location = loc
        self.log.info('Will add %s of %s', pic, taxon)

        # Copy files to gallery
        dryrun = False
        self.runSystemCommand(f'cp {filename} {dest}', dryrun)
        self.runSystemCommand(f'convert {filename} -resize 500x500 {config.dirPicsBase}medium/{basename}', dryrun)
        self.runSystemCommand(f'convert {filename} -resize 180x180 {config.dirPicsBase}thumbs/{basename}', dryrun)

        # Save to DB
        self.pictureCache.save(pic)

        # Update caches
        taxon.addPicture(pic)
        loc.addPicture(pic)
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
    
    def addExcursionFromGeoTrack(self, filename: str) -> Expedition:
        """Add an excursion from a GeoTrack file."""
        self.log.info('Adding excursion from %s', filename)

        # Check file exists
        if not os.path.exists(filename):
            raise PynorpaException(f"Le GeoTrack n'existe pas : {filename}")
        
        # Load track
        track = GeoTrack(filename)
        track.loadData()

        # Find location
        loc = self.locationCache.getClosest(track.getCenter().latitude, track.getCenter().longitude)
        self.log.info('GeoTrack is closest to %s', loc)
        if not loc:
            raise PynorpaException(f"Le GeoTrack ne correspond à aucun lieu : {filename}")

        # Create Expedition
        name = TextTools.removeDigits(track.name)
        excursion = Expedition(-1, name, None, loc.getIdx(), 
                               DateTools.datetimeToLocal(track.tStart), 
                               DateTools.datetimeToLocal(track.tEnd), 
                               os.path.basename(filename).removesuffix('.gpx'))
        self.log.info('Adding %s', excursion)

        # Set location and pictures
        self.expeditionCache.setLocationPictures(excursion, loc)

        # Copy GPX file
        self.runSystemCommand(f'cp {filename} {config.dirExportGeoTrack}')
        return excursion
    
    def runSystemCommand(self, cmd: str, dryrun=False):
        """Run a system command."""
        if dryrun:
            self.log.info('dryrun: %s', cmd)
        else:
            os.system(cmd)
        
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
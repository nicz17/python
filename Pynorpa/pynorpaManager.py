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
from taxon import TaxonCache, Taxon, TaxonRank
from expedition import Expedition, ExpeditionCache
from iNatApiRequest import INatApiRequest, INatTaxon


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
            self.log.warning('Invalid photo size %s', info.getSizeString())
            #raise PynorpaException(f'Taille invalide : {info.getSizeString()}')

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
    
    def addTaxonFromINat(self, name: str, module):
        """Add a taxon and its ancestors if needed. Query iNat API for the ancestors."""
        taxon = self.taxonCache.findByName(name)
        if taxon:
            self.log.info(f'{name} already in DB: {taxon}')
            raise PynorpaException(f'Le taxon existe déjà :\n{taxon}')
        
        self.log.info(f'Will query iNat API for ancestors of {name}')
        if not name:
            raise PynorpaException(f'Nom de taxon invalide: {name}')

        # iNat API request
        req = INatApiRequest()
        inatTaxon = req.getTaxonFromName(name)
        if not inatTaxon:
            self.log.error(f'Failed to find iNat id for taxon name {name}')
            raise PynorpaException(f'iNat ne connait pas {name}')
        else:
            self.log.info(f'Found {inatTaxon}')
        
        ancestors = req.getAncestors(inatTaxon.id)
        if ancestors is None or len(ancestors) == 0:
            self.log.error(f'Failed to find iNat ancestors for {inatTaxon.id}')
            raise PynorpaException(f'iNat ne trouve pas la hiérarchie de {name} ({inatTaxon.id})')
        
        # Loop over ancestors, look if already in Panorpa DB
        self.log.info(f'Found {len(ancestors)} ancestors')
        taxa = []
        idxParent = None
        for ancestor in ancestors:
            self.log.info(ancestor)
            taxon = self.taxonCache.findByName(ancestor.name)
            if taxon:
                self.log.info(f'  Found: {taxon}')
                idxParent = taxon.idx
            else:
                taxon = self.taxonCache.createFromINatTaxon(ancestor, idxParent)
                self.log.info(f'  Missing: {taxon}')
                idxParent = taxon.idx
            taxa.append(taxon)

        # Add the taxon itself
        taxon = Taxon(-1*inatTaxon.id, name, name, inatTaxon.rank.upper(), idxParent, 0, False)
        self.log.info(f'  Missing: {taxon}')
        taxa.append(taxon)

        # Ask user for confirmation
        iNewTaxa = 0
        msgConfirm = ''
        taxon: Taxon
        for taxon in taxa:
            msgConfirm += 'Existe' if taxon.idx > 0 else 'Manque'
            msgConfirm += f' : {taxon.getRankFr()} {taxon.name}\n'
            if taxon.idx < 0:
                iNewTaxa += 1
        module.setLoadingIcon(True)
        reply = mb.askyesno(name, f'Ajouter {iNewTaxa} taxons ?', detail=msgConfirm)
        if not reply:
            self.log.error(f'Canceled by user.')
            raise PynorpaException(f'Annulé.')
        self.saveINatTaxa(taxa)
        
    def saveINatTaxa(self, taxa: list[Taxon], cbkStatus=None):
        """Save new taxa to DB"""
        iNewTaxa = 0
        parent = None
        idxParent = None
        for taxon in taxa:
            if taxon.idx < 0:
                if taxon.idxParent < 0:
                    taxon.idxParent = idxParent
                if taxon.parent is None and parent is not None and parent.idx == idxParent:
                    taxon.parent = parent
                self.log.info(f'Will save {taxon}')
                self.taxonCache.insert(taxon)
                self.log.info(f'Saved {taxon}')
                iNewTaxa += 1
            idxParent = taxon.idx
            parent = taxon
        msg = f'Créé {iNewTaxa} nouveaux taxons.'
        if cbkStatus:
            cbkStatus(msg)
        else:
            mb.showinfo('Succès', msg)
        return taxon
    
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
    #mgr.addLocation(config.dirSourceGeoTrack + 'Lauenensee250216.gpx')
    #mgr.addPicture('vanessa-cardui004.jpg', None)
    mgr.addTaxonFromINat('Solorina saccata')

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testManager()
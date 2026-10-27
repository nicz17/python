"""Module for various quality and consistency checks."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
import os

from LocationCache import LocationCache
from moduleReselection import ReselectionContext
from PhotoInfo import WebPhoto
from picture import PictureCache, Picture
from pynorpaManager import PynorpaManager
from taxon import TaxonCache, TaxonRank
from iNatApiRequest import INatApiRequestObs, INatObs
from Timer import Timer


class QualityIssue():
    """Class QualityIssue"""
    log = logging.getLogger("QualityIssue")

    def __init__(self, idx: int, desc: str, details: str, pic: Picture):
        """Constructor."""
        self.idx = idx
        self.desc = desc
        self.details = details
        self.pic = pic
        self.cbkLink = None
        self.extUrl = None

    def setLink(self, cbkLink):
        """Setter for link"""
        self.cbkLink = cbkLink

    def getIdx(self) -> int:
        """Getter for idx"""
        return self.idx
    
    def getKind(self) -> str:
        """Get kind of object causing this issue."""
        if self.cbkLink is None:
            return 'Autre'
        objClass = type(self.cbkLink).__name__
        if objClass == 'Picture':
            return 'Photo'
        if objClass == 'Location':
            return 'Lieu'
        if objClass == 'Taxon':
            return 'Taxon'
        if objClass == 'INatObs':
            return 'iNat'
        if objClass == 'ReselectionContext':
            return 'iNat'
        return objClass

    def getDesc(self) -> str:
        """Getter for desc"""
        return self.desc
    
    def getDetails(self) -> str:
        """Getter for details"""
        return self.details

    def getPic(self) -> Picture:
        """Getter for pic"""
        return self.pic

    def getLink(self):
        """Getter for link"""
        return self.cbkLink

    def setExternalUrl(self, url: str):
        self.extUrl = url

    def getExternalUrl(self) -> str:
        return self.extUrl

    def __str__(self):
        return f'QualityIssue {self.idx}: {self.desc}'
    

class QualityChecker():
    """Class for various quality and consistency checks."""
    log = logging.getLogger("QualityChecker")

    def __init__(self):
        """Constructor."""
        self.issues = []
        self.locCache = LocationCache()
        self.picCache = PictureCache()
        self.taxCache = TaxonCache()

    def runAllChecks(self):
        """Run all quality checks."""
        self.checkPictureFiles()
        self.checkEmptyTaxa()
        self.checkLocations()
        self.checkLowQualityPics()
        self.log.info(f'Found {self.countIssues()} quality issues.')

    def addIssue(self, desc: str, details: str, pic: Picture, link=None):
        """Add a quality issue."""
        idx = self.countIssues() + 1
        issue = QualityIssue(idx, desc, details, pic)
        issue.setLink(link)
        self.issues.append(issue)

    def getIssues(self) -> list[QualityIssue]:
        """Get list of detected quality issues."""
        return self.issues
    
    def countIssues(self) -> int:
        """Count the detected quality issues."""
        return len(self.issues)

    def checkPictureFiles(self):
        """Check picture files exist."""
        for pic in sorted(self.picCache.getPictures(), key=lambda pic: pic.shotAt):
            filename = f'{config.dirPictures}{pic.getFilename()}'
            if not os.path.exists(filename):
                self.log.error(f'Missing picture file {pic.getFilename()} on {pic.getShotAt()} in {pic.getLocationName()}')
                details = f'{pic.getShotAt()} à {pic.getLocationName()}'
                self.addIssue(f"La photo {pic.getFilename()} n'existe pas", details, pic, pic)

    def checkEmptyTaxa(self):
        """Check that each taxon has observations."""
        # Check that Species taxa have pictures
        for taxon in self.taxCache.getForRank(TaxonRank.SPECIES):
            if taxon.countAllPictures() == 0:
                self.log.error(f'Taxon has no pictures: {taxon}')
                self.addIssue(f"Le taxon {taxon.getName()} n'a pas d'observations", taxon, None, taxon)
        # Check that Genus taxa have pictures
        for taxon in self.taxCache.getForRank(TaxonRank.GENUS):
            if taxon.countAllPictures() == 0:
                self.log.error(f'Taxon has no pictures: {taxon}')
                self.addIssue(f"Le genre {taxon.getName()} n'a pas d'observations", taxon, None, taxon)
        # Check that Order taxa have children
        for taxon in self.taxCache.getForRank(TaxonRank.ORDER):
            if len(taxon.getChildren()) == 0:
                self.log.error(f'Taxon has no children: {taxon}')
                self.addIssue(f"Le taxon {taxon.getName()} n'a pas d'enfants", taxon, None, taxon)


    def checkLowQualityPics(self):
        """Check for species with many pictures, some of which are bad quality."""
        minPics = 5
        for taxon in self.taxCache.getForRank(TaxonRank.SPECIES):
            if taxon.countAllPictures() >= minPics:
                pic: Picture
                for pic in taxon.getPictures():
                    if pic.getRating() < 3:
                        self.log.warning(f'Taxon {taxon.getName()} has a low-quality pic {pic}')
                        details = f"Photo de qualité {pic.getRating()} avec {taxon.countAllPictures()} photos"
                        self.addIssue(f"La photo {pic.getFilename()} pourrait être effacée", details, pic, pic)

    def checkLocations(self):
        """Find Locations with too short descriptions or too few pictures."""
        minDescLen = 25
        minPicsInLoc = 2
        for loc in self.locCache.getLocations():
            desc = loc.getDesc()
            if len(desc) < minDescLen:
                self.log.error(f'Location has short description: {loc}: {desc}')
                self.addIssue(f"Le lieu {loc.getName()} a une description très courte", desc, None, loc)
            nPics = len(loc.getPictures())
            if nPics < minPicsInLoc:
                self.log.info(f'Location has few pictures: {loc}: {nPics} pictures')
                details = ''
                for pic in loc.getPictures():
                    details += pic.getFilename() + ' '
                msg = f"Le lieu {loc.getName()} n'a que {nPics} photos"
                pic = None
                if nPics == 0:
                    msg = f"Le lieu {loc.getName()} n'a pas de photos"
                if nPics == 1:
                    msg = f"Le lieu {loc.getName()} n'a qu'une photo"
                    pic = loc.getPictures()[0]
                self.addIssue(msg, details, pic, loc)

class QualityCheckerINatObs():
    """Check for iNat species-level observations missing on Pynorpa."""
    log = logging.getLogger("QualityCheckerINatObs")
    perPage = 12

    def __init__(self, year: int, month: int, cbkProgress=None):
        """Constructor."""
        self.year = year
        self.month = month
        self.cbkProgress = cbkProgress
        self.issues = []
        self.taxCache = TaxonCache()
        self.manager = PynorpaManager()

    def run(self):
        """Run the checks."""
        # First find the number of observations without details.
        timer = Timer()
        req = INatApiRequestObs(self.year, self.month)
        count = req.sendCountRequest()
        if count is None:
            self.log.error('Count request failed')
            if self.cbkProgress:
                self.cbkProgress(0.0, 'Echec de chargement des observations')
            return
        
        pages = count//self.perPage + 1
        fetched = 0
        self.log.info(f'Observation count is {count}, requiring {pages} pages')
        if self.cbkProgress:
            self.cbkProgress(0.0, f'Vérification de {count} observations sur {pages} pages')

        # Send requests over several pages with a progress bar
        for page in range(1, pages+1):
            data = req.sendRequest(page, self.perPage)
            lobs = req.readResponse(data)
            error = ''
            if lobs:
                fetched += len(lobs) 
                for obs in lobs:
                    self.checkTaxon(obs)
            else:
                error = ' Erreur: pas de réponse'
            if self.cbkProgress:
                self.cbkProgress(100.0*page/pages, f'Page {page} sur {pages}{error}')
        if self.cbkProgress:
            self.cbkProgress(100.0, f'Vérifié {fetched}/{count} observations en {timer.getElapsed()}')

    def checkTaxon(self, obs: INatObs):
        """Check if the iNat obs taxon is missing in Paynorpa."""
        taxname = obs.getTaxon()
        taxon = self.taxCache.findByName(taxname)
        if not taxon:
            # Check if it is a known synonym
            taxon = self.taxCache.findBySynonym(taxname)
            if taxon:
                self.log.info(f'{taxname} is a synonym of {taxon}')
        if not taxon:
            # Add as an issue
            # TODO also store bad quality Android obs to ignore
            self.log.info(f'Taxon {taxname} observed on {obs.sAt} missing in Pynorpa - {obs.getObsUrl()}')
            matches = self.manager.findMatchingSelections(obs)
            matchinfo = 'Pas de sélections correspondates'
            closest = None if len(matches) == 0 else matches[0]
            if len(matches) == 1:
                matchinfo = f'Correspond à {matches[0].getNameNoExt()}'
            elif len(matches) > 1:
                matchinfo = f'{len(matches)} sélections correspondates'
            desc = f'Espèce manquante : {taxname} ({obs.getPlace()})'
            details = f'Observé le {obs.getAt()}\nà {obs.getPlace()}\n{obs.getObsUrl()}\n{matchinfo}'
            webPhoto = WebPhoto(obs.getPhotoUrl(), f'{taxname} sur iNaturalist')
            issue = QualityIssue(obs.id, desc, details, webPhoto)
            issue.setLink(ReselectionContext(obs.dtAt, closest))
            issue.setExternalUrl(obs.getObsUrl())
            self.issues.append(issue)
            # TODO store these found issues in a json file? on demand in module (export table)

    def getIssues(self) -> list[QualityIssue]:
        """Get list of detected quality issues."""
        return self.issues


def testQuality():
    """Unit test for QualityChecker."""
    checker = QualityChecker()
    checker.runAllChecks()

def testQualityINatObs():
    """Unit test for QualityCheckerINatObs."""
    checker = QualityCheckerINatObs(2026, 4)
    checker.run()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    #testQuality()
    testQualityINatObs()
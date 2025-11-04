"""Module for various quality and consistency checks."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
import os

from LocationCache import LocationCache
from picture import PictureCache, Picture
from taxon import TaxonCache, TaxonRank


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
        """Find Locations with too short descriptions."""
        minDescLen = 25
        for loc in self.locCache.getLocations():
            desc = loc.getDesc()
            if len(desc) < minDescLen:
                self.log.error(f'Location has short description: {loc}: {desc}')
                self.addIssue(f"Le lieu {loc.getName()} a une description très courte", desc, None, loc)


def testQuality():
    """Unit test for QualityChecker."""
    checker = QualityChecker()
    checker.runAllChecks()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testQuality()
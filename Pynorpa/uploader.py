"""
Upload generated Pynorpa HTML files and photos
to www.tf79.ch using FTP.
"""

import config
import ftplib
import logging
import os
import time

from picture import Picture, PictureCache
from taxon import Taxon, TaxonRank
from Timer import *

class Uploader:
    """Upload files to website using FTP."""
    log = logging.getLogger('Uploader')

    def __init__(self, bDryRun=False) -> None:
        self.oSession = None
        self.tLastUpload = self.getLastUpload()
        self.bDryRun = bDryRun
        self.log.info('Last upload at %s', self.timeToStr(self.tLastUpload))
        self.cache = None

    def uploadModified(self):
        """Upload modified pictures and their pages."""
        self.log.info('Uploading modified pictures and pages')
        self.cache = PictureCache()
        picsModified = self.cache.fetchPicsToUpload()
        taxaModified = set()
        for pic in picsModified:
            taxon: Taxon
            taxon = pic.getTaxon()
            while (taxon is not None):
                taxaModified.add(taxon)
                taxon = taxon.getParent()
            
        self.log.info(f'Fetched {len(picsModified)} pictures in {len(taxaModified)} taxa')
        # TODO upload pics, medium, thumbs and pages
        for pic in picsModified:
            self.log.info(f'Will upload {pic}')
        for taxon in taxaModified:
            self.log.info(f'Will upload page for {taxon}')

    def uploadAll(self):
        """Upload base files, photos and thumbs more recent than last upload."""
        self.log.info('Uploading all files as needed')
        oTimer = Timer()
        self.connect()
        self.uploadBaseFiles()
        self.uploadThumbs()
        self.uploadPhotos()
        self.setLastUpload()
        self.quit()
        self.log.info('Done uploading in %s', oTimer.getElapsed())

    def uploadSinglePhoto(self, pic: Picture):
        """Upload a single picture file."""
        filename = f'{config.dirWebExport}photos/{pic.getFilename()}'
        self.log.info('Will upload %s', filename)
        self.connect()
        self.upload(filename, 'photos/')
        self.quit()

    def uploadSingleTaxon(self, taxon: Taxon):
        """Upload a single taxon page."""
        pageName = self.getTaxonPage(taxon)
        filename = f'{config.dirWebExport}pages/{pageName}'
        self.log.info('Will upload %s for taxon %s', filename, taxon)
        if not os.path.exists(filename):
            self.log.error(f'Fle to upload does not exist: {filename}')
            return
        self.connect()
        self.upload(filename, 'pages/')
        self.quit()

    def uploadBaseFiles(self):
        """Upload the base files like index, locations, links etc."""
        self.log.info('Uploading base files')
        aTypes = ['*.html', '*.js']
        # aFiles = []
        # for sType in aTypes:
        #     aFiles.extend(glob.glob(config.sDirExport + sType))
        aFiles = [f'{config.dirWebExport}liens.html']
        for sFile in aFiles:
            if (self.needsUpload(sFile)):
                self.log.info('  %s has been modified, will upload', sFile)
                self.upload(sFile)

    def uploadPhotos(self):
        """Upload the photo JPG files."""
        pass

    def uploadThumbs(self):
        """Upload the photo thumbnail files."""
        pass

    def upload(self, sFilename: str, dir=None):
        """Upload the specified file to FTP."""
        if self.oSession:
            self.log.info('Uploading %s', sFilename)
            if dir:
                self.oSession.cwd(dir)
            oFile = open(sFilename, 'rb')
            self.oSession.storbinary('STOR ' + os.path.basename(sFilename), oFile)
            oFile.close()

    def connect(self):
        """Connect to FTP server."""
        if not self.bDryRun:
            self.log.info('Connecting to FTP %s as %s', config.ftpAddress, config.ftpUser)
            try:
                self.oSession = ftplib.FTP(config.ftpAddress, config.ftpUser, config.ftpPassword)
                self.log.info('Connected to FTP: %s', self.oSession.getwelcome())
                self.oSession.cwd('httpdocs/nature/')
            except ftplib.error_perm:
                self.log.error('Failed to connect or cwd')
                self.quit()

    def quit(self):
        """Close the connection if it is still open."""
        if self.oSession:
            self.log.info('Closing FTP connection')
            self.oSession.close()

    def needsUpload(self, sFile):
        #self.log.info('  %s modifed at %s', sFile, self.timeToStr(self.getModifiedAt(sFile)))
        return self.getModifiedAt(sFile) > self.tLastUpload

    def setLastUpload(self):
        if not self.bDryRun:
            self.log.info('Setting last-upload timestamp file to now')
            os.system('touch last-upload')

    def getLastUpload(self):
        return self.getModifiedAt('last-upload')
    
    def getModifiedAt(self, sFile):
        return os.path.getmtime(sFile)
    
    def timeToStr(self, tAt):
        return time.strftime('%Y.%m.%d %H:%M:%S', time.gmtime(tAt))
    
    def getTaxonPage(self, taxon: Taxon) -> str:
        """Return the file name for the specified taxon."""
        if taxon is None:
            return None
        match taxon.getRank():
            case TaxonRank.SPECIES:
                return f"{taxon.getName().replace(' ', '-').lower()}.html"
            case TaxonRank.GENUS | TaxonRank.FAMILY:
                # return None if no pictures
                if len(taxon.getPictures()) > 0:
                    return f'{taxon.getName().lower()}.html'
                return None
            case TaxonRank.ORDER | TaxonRank.PHYLUM:
                return f'{taxon.getName()}.html'
            case TaxonRank.CLASS | TaxonRank.KINGDOM:
                return None
        return None
    
    def getTaxonDir(self, taxon: Taxon) -> str:
        """Return the path for the specified taxon."""
        pass

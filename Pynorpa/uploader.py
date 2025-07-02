"""
Upload generated Pynorpa HTML files and photos
to www.tf79.ch using FTP.
"""

import config
import ftplib
import logging
import os

from appParam import AppParamCache
from LocationCache import Location
from picture import Picture, PictureCache
from taxon import Taxon, TaxonRank
from Timer import *

class Uploader:
    """Upload files to website using FTP."""
    log = logging.getLogger('Uploader')

    def __init__(self, bDryRun=False) -> None:
        self.oSession = None
        self.bDryRun = bDryRun
        self.log.info(f'Dry-run: {bDryRun}')
        self.apCache = AppParamCache()
        self.picCache = None

    def countModified(self) -> int:
        """Returns the number of pics to upload."""
        self.picCache = PictureCache()
        picsModified = self.picCache.fetchPicsToUpload()
        return len(picsModified)

    def uploadModified(self):
        """Upload modified pictures and their pages."""
        self.log.info('Uploading modified pictures and pages')
        oTimer = Timer()
        self.connect()

        # Fetch pics, taxa and locations to upload
        self.picCache = PictureCache()
        picsModified = self.picCache.fetchPicsToUpload()
        taxaModified = set()
        locsModified = set()
        for pic in picsModified:
            self.log.info(f'Will upload {pic}')
            taxon: Taxon
            taxon = pic.getTaxon()
            while (taxon is not None):
                taxaModified.add(taxon)
                taxon = taxon.getParent()
            loc = pic.getLocation()
            if loc:
                locsModified.add(loc)
        self.log.info(f'Fetched {len(picsModified)} pictures in {len(taxaModified)} taxa and {len(locsModified)} locations')

        # Upload pics, medium, thumbs
        self.uploadPhotos(picsModified, config.dirPictures, 'photos/')
        self.uploadPhotos(picsModified, f'{config.dirPicsBase}medium/', 'medium/')
        self.uploadPhotos(picsModified, f'{config.dirPicsBase}thumbs/', 'thumbs/')

        # Upload taxon pages if they exist
        taxaBase  = []
        taxaPages = []
        for taxon in taxaModified:
            filename = self.getTaxonPage(taxon)
            if filename:
                self.log.debug(f'Will upload page for {taxon}')
                dir = self.getTaxonDir(taxon)
                if dir is None:
                    taxaBase.append(f'{config.dirWebExport}{filename}')
                else:
                    taxaPages.append(f'{config.dirWebExport}{dir}{filename}')
        self.uploadMulti(taxaBase,  'base taxa')
        self.uploadMulti(taxaPages, 'page taxa', 'pages/')

        # Upload modified locations
        locFiles = []
        loc: Location
        for loc in locsModified:
            filename = f'{config.dirWebExport}lieu{loc.getIdx()}.html'
            locFiles.append(filename)
        self.uploadMulti(locFiles, 'location')

        # Upload index and other base html pages
        # TODO generate and upload taxa.json
        htmlFiles = []
        homePages = ['index', 'classification', 'latest', 'locations', 'noms-latins', 'noms-verna', 'expeditions', 'liens']
        for page in homePages:
            filename = f'{config.dirWebExport}{page}.html'
            htmlFiles.append(filename)
        self.uploadMulti(htmlFiles, 'home')

        self.quit()
        self.apCache.setLastUploadAt()
        self.log.info('Done uploading modifs in %s', oTimer.getElapsed())

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
        if pageName is None:
            self.log.warning(f'No page for {taxon}, will not upload')
            return
        
        dir = self.getTaxonDir(taxon)
        filename = f'{config.dirWebExport}{"" if dir is None else dir}{pageName}'
        self.log.info('Will upload %s for taxon %s', filename, taxon)
        if not os.path.exists(filename):
            self.log.error(f'File to upload does not exist: {filename}')
            return
        self.connect()
        self.upload(filename, dir)
        self.quit()

    def uploadPhotos(self, pics: list[Picture], localDir: str, ftpDir: str):
        """Upload the photo/medium/thumbs JPG files."""
        self.log.info(f'Uploading {len(pics)} pics from {localDir} to {ftpDir}')
        files = []
        for pic in pics:
            filename = f'{localDir}{pic.filename}'
            if not os.path.exists(filename):
                self.log.error(f'Missing file: {filename}')
            else:
                files.append(filename)
        self.uploadMulti(files, 'pics', ftpDir)

    def upload(self, filename: str, dir=None):
        """Upload the specified file to FTP."""
        if self.oSession:
            self.log.info('Uploading %s', filename)
            if dir:
                self.oSession.cwd(dir)
                self.log.info(f'Now in ftp:{self.oSession.pwd()}')
            with open(filename, 'rb') as file:
                self.oSession.storbinary('STOR ' + os.path.basename(filename), file)
            if dir:
                self.oSession.cwd('..')
                self.log.info(f'Now in ftp:{self.oSession.pwd()}')

    def uploadMulti(self, files: list[str], kind: str, dir=None):
        """Upload multiple files to the same FTP dir."""
        sDryRun = '[dryrun] ' if self.bDryRun else ''
        self.log.info(f'{sDryRun}Uploading {len(files)} {kind} files to {dir}')
        if self.oSession:
            if dir:
                self.oSession.cwd(dir)
                self.log.debug(f'Now in ftp:{self.oSession.pwd()}')
            for filename in files:
                with open(filename, 'rb') as file:
                    self.oSession.storbinary('STOR ' + os.path.basename(filename), file)
            if dir:
                self.oSession.cwd('..')
                self.log.debug(f'Now in ftp:{self.oSession.pwd()}')

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
    
    def getModifiedAt(self, sFile):
        return os.path.getmtime(sFile)
    
    def getTaxonPage(self, taxon: Taxon) -> str:
        """Return the file name for the specified taxon, or None if no page."""
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
        if taxon is None:
            return None
        match taxon.getRank():
            case TaxonRank.SPECIES | TaxonRank.GENUS | TaxonRank.FAMILY:
                return 'pages/'
            case _:
                return None

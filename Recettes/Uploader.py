"""
Upload generated recipe HTML files and photos
to www.tf79.ch using FTP.
"""

import logging
import config
import ftplib
import getpass
import glob
import os
import time

class Uploader:
    """Upload files to website using FTP."""
    log = logging.getLogger('Uploader')

    def __init__(self, bDryRun = False) -> None:
        self.oSession = None
        self.tLastUpload = self.getLastUpload()
        self.bDryRun = bDryRun
        self.log.info('Last upload at %s', self.timeToStr(self.tLastUpload))

    def uploadAll(self):
        """Upload base files, recipes, photos and thumbs more recent than last upload."""
        self.log.info('Uploading all files as needed')
        self.connect()
        self.uploadBaseFiles()
        self.uploadRecipes()
        self.uploadPhotos()
        self.uploadThumbs()
        self.setLastUpload()
        self.quit()

    def uploadBaseFiles(self):
        """Upload the base files like index, chapters, thanks, biblio etc."""
        self.log.info('Uploading base files')
        aBaseFiles = glob.glob(config.sDirExport + '*.html')
        for sFile in aBaseFiles:
            if (self.needsUpload(sFile)):
                self.log.info('  %s has been modified, will upload', sFile)
                self.upload(sFile)

    def uploadRecipes(self):
        """Upload the recipe HTML files."""
        aFiles = glob.glob(config.sDirPages + '*.html')
        self.log.info('Uploading from %d recipes', len(aFiles))
        if self.oSession:
            self.oSession.cwd('html/')
        for sFile in aFiles:
            sTexFile = config.sDirSources + os.path.basename(sFile).replace('.html', '.tex')
            if (self.needsUpload(sTexFile) and self.needsUpload(sFile) ):
                self.log.info('  %s has been modified, will upload recipe', sTexFile)
                self.upload(sFile)
        if self.oSession:
            self.oSession.cwd('../')

    def uploadPhotos(self):
        """Upload the recipe JPG files."""
        aPhotos = glob.glob(config.sDirPhotos + '*.jpg')
        self.log.info('Uploading from %d photos', len(aPhotos))
        if self.oSession:
            self.oSession.cwd('photos/')
        for sFile in aPhotos:
            if (self.needsUpload(sFile)):
                self.log.info('  %s has been modified, will upload', sFile)
                self.upload(sFile)
        if self.oSession:
            self.oSession.cwd('../')

    def uploadThumbs(self):
        """Upload the recipe thumbnail files."""
        aFiles = glob.glob(config.sDirThumbs + '*.jpg')
        self.log.info('Uploading from %d thumbs', len(aFiles))
        if self.oSession:
            self.oSession.cwd('thumbs/')
        for sFile in aFiles:
            if (self.needsUpload(sFile)):
                self.log.info('  %s has been modified, will upload', sFile)
                self.upload(sFile)
        if self.oSession:
            self.oSession.cwd('../')

    def upload(self, sFilename):
        """Upload the specified file to FTP."""
        if self.oSession:
            self.log.info('Uploading %s', sFilename)
            oFile = open(sFilename, 'rb')
            self.oSession.storbinary('STOR ' + os.path.basename(sFilename), oFile)
            oFile.close() 

    def test(self):
        self.log.info('Testing upload of readme')
        self.connect()
        self.upload(config.sDirExport + 'readme.html')
        self.quit()

    def connect(self):
        """Connect to FTP server. Ask user for password."""
        if not self.bDryRun:
            self.log.info('Connecting to FTP %s as %s', config.sFtpAddress, config.sFtpUser)
            sFtpPasswd = getpass.getpass(prompt = 'FTP password: ')
            try:
                self.oSession = ftplib.FTP(config.sFtpAddress, config.sFtpUser, sFtpPasswd)
                self.log.info('Connected to FTP: %s', self.oSession.getwelcome())
                self.oSession.cwd('httpdocs/recettes/')
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

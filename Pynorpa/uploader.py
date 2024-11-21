"""
Upload generated Pynorpa HTML files and photos
to www.tf79.ch using FTP.
"""

import logging
import config
import ftplib
import glob
import os
import time
from Timer import *

class Uploader:
    """Upload files to website using FTP."""
    log = logging.getLogger('Uploader')

    def __init__(self, bDryRun=False) -> None:
        self.oSession = None
        self.tLastUpload = self.getLastUpload()
        self.bDryRun = bDryRun
        self.log.info('Last upload at %s', self.timeToStr(self.tLastUpload))

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

    def uploadBaseFiles(self):
        """Upload the base files like index, locations, links etc."""
        self.log.info('Uploading base files')
        aTypes = ['*.html', '*.js']
        # aFiles = []
        # for sType in aTypes:
        #     aFiles.extend(glob.glob(config.sDirExport + sType))
        aFiles = ['export/liens.html']
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

    def upload(self, sFilename):
        """Upload the specified file to FTP."""
        if self.oSession:
            self.log.info('Uploading %s', sFilename)
            oFile = open(sFilename, 'rb')
            self.oSession.storbinary('STOR ' + os.path.basename(sFilename), oFile)
            oFile.close()

    def connect(self):
        """Connect to FTP server. Ask user for password."""
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

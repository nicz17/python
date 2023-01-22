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

    def __init__(self) -> None:
        self.oSession = None
        self.tLastUpload = self.getLastUpload()
        self.log.info('Last upload at %s', self.timeToStr(self.tLastUpload))

    def uploadBaseFiles(self):
        """Uploads the base files like index, thanks, biblio etc."""
        self.log.info('Uploading base files')
        aBaseFiles = ['index.html', 'biblio.html', 'ingredients.html',
                      'news.html', 'readme.html', 'thanks.html', 'thumbs.html']
        for sName in aBaseFiles:
            sFile = config.sDirExport + sName
            if (self.needsUpload(sFile)):
                self.log.info('  %s has been modified, will upload', sName)
                self.upload(sFile)

    def uploadChapters(self):
        """Upload all the chapters HTML files."""
        aChapters = glob.glob(config.sDirExport + 'chapter*.html')
        self.log.info('Uploading %d chapters', len(aChapters))
        for sChap in aChapters:
            self.upload(sChap)

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
        self.log.info('Uploading %s to FTP server', sFilename)
        oFile = open(sFilename, 'rb')
        self.oSession.storbinary('STOR ' + os.path.basename(sFilename), oFile)
        oFile.close() 

    def test(self):
        self.log.info('Testing upload of thanks')
        self.connect()
        #self.upload(config.sDirExport + 'thanks.html')
        #self.uploadChapters()
        #self.setLastUpload()
        #self.uploadBaseFiles()
        self.uploadPhotos()
        self.uploadThumbs()
        self.quit()

    def connect(self):
        """Connect to FTP server. Ask user for password."""
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
        self.log.info('Setting last-upload timestamp file to now')
        #os.system('touch last-upload')

    def getLastUpload(self):
        return self.getModifiedAt('last-upload')
    
    def getModifiedAt(self, sFile):
        return os.path.getmtime(sFile)
    
    def timeToStr(self, tAt):
        return time.strftime('%Y.%m.%d %H:%M:%S', time.gmtime(tAt))

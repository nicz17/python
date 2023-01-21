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

class Uploader:
    """Upload files to website using FTP."""
    log = logging.getLogger('Uploader')

    def __init__(self) -> None:
        self.oSession = None

    def uploadBaseFiles(self):
        pass

    def uploadChapters(self):
        """Upload all the chapters HTML files."""
        aChapters = glob.glob(config.sDirExport + 'chapter*.html')
        self.log.info('Uploading %d chapters', len(aChapters))
        for sChap in aChapters:
            self.upload(sChap)

    def upload(self, sFilename):
        """Upload the specified file to FTP."""
        self.log.info('Uploading %s to FTP server', sFilename)
        oFile = open(sFilename, 'rb')
        self.oSession.storbinary('STOR ' + os.path.basename(sFilename), oFile)
        oFile.close() 

    def test(self):
        self.log.info('Testing upload of biblio')
        self.connect()
        #self.upload(config.sDirExport + 'biblio.html')
        self.uploadChapters()
        self.quit()

    def connect(self):
        self.log.info('Connecting to FTP %s as %s', config.sFtpAddress, config.sFtpUser)
        sFtpPasswd = getpass.getpass(prompt = 'FTP password: ')
        try:
            self.oSession = ftplib.FTP(config.sFtpAddress, config.sFtpUser, sFtpPasswd)
            self.log.info('Connected to FTP: %s', self.oSession.getwelcome())
            self.oSession.cwd('httpdocs/recettes/')
        except ftplib.error_perm:
            self.log.error('Failed to connect or cwd')
        finally:
            self.quit()

    def quit(self):
        if self.oSession:
            self.log.info('Closing FTP connection')
            self.oSession.close()

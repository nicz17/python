"""
Upload generated recipe HTML files and photos
to www.tf79.ch using FTP.
"""

import logging
import config
import ftplib
import getpass

class Uploader:
    """Upload files to website using FTP."""
    log = logging.getLogger('Uploader')

    def __init__(self) -> None:
        self.oSession = None

    def upload(self, sPath, sFilename):
        """Upload the specified file to FTP."""
        self.log.info('Uploading to %s to FTP server', sPath + sFilename)
        oFile = open(sPath + sFilename, 'rb')
        self.oSession.storbinary('STOR ' + sFilename, oFile)
        oFile.close() 

    def test(self):
        self.log.info('Testing upload of biblio')
        self.connect()
        self.upload(config.sDirExport, 'biblio.html')
        self.quit()

    def connect(self):
        self.log.info('Connecting to FTP %s as %s', config.sFtpAddress, config.sFtpUser)
        sFtpPasswd = getpass.getpass(prompt = 'FTP password: ')
        self.oSession = ftplib.FTP(config.sFtpAddress, config.sFtpUser, sFtpPasswd)
        self.log.info('Connected to FTP: %s', self.oSession.getwelcome())
        self.oSession.cwd('httpdocs/recettes/')

    def quit(self):
        self.log.info('Closing FTP connection')
        if self.oSession:
            self.oSession.close()

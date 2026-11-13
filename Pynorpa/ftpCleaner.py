"""
List and remove files on the FTP server that are no more needed.
"""

import config
import ftplib
import logging
import os

from appParam import AppParamCache
from LocationCache import Location
from picture import Picture, PictureCache
from taxon import Taxon, TaxonRank
from Timer import Timer


class FTPCleaner:
    log = logging.getLogger('FTPCleaner')

    def __init__(self):
        self.log.info('Constructor')
        self.oSession = None

    def listFiles(self, dir: str) -> list[str]:
        """Returns a list of files in the specified dir."""
        self.log.info(f'Listing files in {dir}')
        self.oSession.cwd(dir)
        files = self.oSession.nlst()
        return files

    def connect(self):
        """Connect to FTP server."""
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

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
from taxon import TaxonCache
from Timer import TimedTask


class FTPFile:
    log = logging.getLogger('FTPFile')

    def __init__(self, path: str, name: str):
        self.path = path
        self.name = name

    def getPath(self) -> str:
        return self.path
    
    def getName(self) -> str:
        return self.name

class FTPCleaner:
    log = logging.getLogger('FTPCleaner')

    def __init__(self):
        self.log.info('Constructor')
        self.oSession = None

    def getFilesToRemove(self) -> list[FTPFile]:
        """Build the list of files to remove from the FTP server."""
        task = TimedTask('Check for files to remove from FTP server')
        taxonCache = TaxonCache()
        result = []
        self.connect()

        # HTML pages
        files = self.listFiles('pages')
        self.log.info(f'Checking {len(files)} HTML pages')
        for file in files:
            #self.log.info(f'  {file}')
            if not file.endswith('.html'):
                continue
            name = file.removesuffix('.html').replace('-', ' ', 1).capitalize()
            if not taxonCache.findByName(name):
                self.log.info(f'  {file}: Unknown taxon name {name}')
                result.append(FTPFile('pages', file))

        # TODO pictures
        # TODO medium
        # TODO thumbs

        self.disconnect()
        task.done()
        return result

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
            self.disconnect()

    def disconnect(self):
        """Close the connection if it is still open."""
        if self.oSession:
            self.log.info('Closing FTP connection')
            self.oSession.close()

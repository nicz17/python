"""
List and remove files on the FTP server that are no more needed.
"""

import config
import ftplib
import logging
import os

from BaseWidgets import ProgressBar
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

    def __str__(self):
        return f'FTPFile {self.path}/{self.name}'

class FTPCleaner:
    log = logging.getLogger('FTPCleaner')

    def __init__(self, progbar: ProgressBar):
        self.log.info('Constructor')
        self.session = None
        self.progbar = progbar

    def getFilesToRemove(self) -> list[FTPFile]:
        """Build the list of files to remove from the FTP server."""
        task = TimedTask('Check for files to remove from FTP server')
        taxonCache = TaxonCache()
        result = []
        self.connect()

        # HTML pages
        path = 'pages'
        files = self.listFiles(path)
        self.log.info(f'Checking {len(files)} HTML pages')
        for file in files:
            if not file.endswith('.html'):
                continue
            name = file.removesuffix('.html').replace('-', ' ', 1).capitalize()
            if not taxonCache.findByName(name):
                self.log.info(f'  {file}: Unknown taxon name {name}')
                result.append(FTPFile(path, file))
        self.progbar.increment()

        result.extend(self.checkPictureKind('photos', f'{config.dirPictures}'))
        #result.extend(self.checkPictureKind('medium', f'{config.dirWebExport}medium/'))
        #result.extend(self.checkPictureKind('thumbs', f'{config.dirWebExport}thumbs/'))

        self.disconnect()
        self.log.info(f'Found {len(result)} files to remove')
        task.done()
        return result

    def checkPictureKind(self, path: str, localPath: str) -> list[FTPFile]:
        result = []
        files = self.listFiles(path)
        self.log.info(f'Checking {len(files)} in {path}')
        for file in files:
            if not file.endswith('.jpg'):
                continue
            filename = f'{localPath}{file}'
            if not os.path.exists(filename):
                self.log.info(f'  Unknown {path} picture: {file}')
                result.append(FTPFile(path, file))
        self.progbar.increment()
        return result

    def listFiles(self, dir: str) -> list[str]:
        """Returns a list of files in the specified dir."""
        self.log.info(f'Listing files in {dir}')
        self.session.cwd(dir)
        files = self.session.nlst()
        self.session.cwd('..')
        return files

    def connect(self):
        """Connect to FTP server."""
        self.log.info(f'Connecting to FTP {config.ftpAddress} as {config.ftpUser}')
        try:
            self.session = ftplib.FTP(config.ftpAddress, config.ftpUser, config.ftpPassword)
            self.log.info(f'Connected to FTP: {self.session.getwelcome()}')
            self.session.cwd('httpdocs/nature/')
        except ftplib.error_perm:
            self.log.error('Failed to connect or cwd')
            self.disconnect()

    def disconnect(self):
        """Close the connection if it is still open."""
        if self.session:
            self.log.info('Closing FTP connection')
            self.session.close()

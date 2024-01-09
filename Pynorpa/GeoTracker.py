"""
 Copy GPX GeoTracking files and apply GPS coords to photos.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import datetime
import glob
#import config
import logging
import os
from PIL import Image, ExifTags
from Timer import *


class GeoTracker:
    """Copy JPG images from Nikon D800 camera."""
    log = logging.getLogger(__name__)
    dirSource = '/home/nicz/Dropbox/GeoTrack/'
    dirTarget = None

    def __init__(self):
        """Constructor."""
        self.log.info('Constructor')
        self.getTargetDirectory()

    def copyFiles(self):
        """Copy GPX GeoTrack files from DropBox."""

        # Check dirs exist
        if not os.path.exists(self.dirTarget):
            self.log.error('Missing target dir %s', self.dirTarget)
            return
        if not os.path.exists(self.dirSource):
            self.log.error('Missing source dir %s', self.dirSource)
            return

        # Glob files
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        filter = self.dirSource + '*' + date.strftime("%y%m") + '*.gpx'
        files = sorted(glob.glob(filter))
        self.log.info('Found %d GeoTrack files in %s', len(files), filter)

        # Copy files
        for file in files:
            self.log.info('Copying %s', os.path.basename(file))
            dest = self.dirTarget + os.path.basename(file)
            os.system(f'cp {file} {dest}')

    def getTargetDirectory(self):
        """Build target directory name from current date."""
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        year  = date.strftime("%Y")
        month = date.strftime("%m")
        self.dirTarget = f'/home/nicz/Pictures/Nature-{year}-{month}/geotracker/'
        self.log.info('Target directory is %s', self.dirTarget)
        
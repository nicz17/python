"""
 Copy JPG images from Nikon D800 camera.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import datetime
import os
import sys
#import config
import logging

class CopyFromCamera:
    """Copy JPG images from Nikon D800 camera."""
    dir = '/home/nzw/Documents/galtest/photos/'
    log = logging.getLogger(__name__)

    def __init__(self):
        """Constructor."""
        self.log.info('Constructor')

    def copyImages(self):
        """Copy JPG images from the mounted camera."""
        targetDir = self.getCurrentTarget()
        self.log.info('Copying images from %s to %s', self.dir, targetDir)

    def getCameraDir(self):
        """Get the current photo dir on the mounted camera."""
        dir = '/mnt/NikonD800/DCIM/'
        return dir

    def getCurrentTarget(self):
        """Get current target image directory. Name is based on year and month."""
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        year = date.strftime("%Y")
        month = date.strftime("%m")
        dir = f'Nature{year}-{month}'
        return dir

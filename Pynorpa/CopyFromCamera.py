"""
 Copy JPG images from Nikon D800 camera.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import datetime
import glob
import os
import sys
#import config
import logging
from PIL import Image

class CopyFromCamera:
    """Copy JPG images from Nikon D800 camera."""
    dir = '/home/nzw/Documents/galtest/photos/'
    log = logging.getLogger(__name__)

    def __init__(self):
        """Constructor."""
        self.log.info('Constructor')

    def copyImages(self):
        """Copy JPG images from the mounted camera."""

        # Find source and target directories
        targetDir = self.getCurrentTarget()
        self.createNatureDirs(targetDir)
        self.log.info('Copying images from %s to %s', self.dir, targetDir)

        # Glob images
        images = sorted(glob.glob(self.dir + '*.jpg'))
        self.log.info('Found %d images:', len(images))
        for img in images:
            self.identify(img)

    def identify(self, img: str):
        """Find details like width, height about the specified image file."""
        im = Image.open(img)
        width, height = im.size
        self.log.info('.. %s %dx%dpx', img, width, height)

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
        dir = f'Nature{year}-{month}/'
        return dir
    
    def createNatureDirs(self, dir):
        """Create photo directories if needed."""
        if not os.path.exists(dir):
            self.log.info('Creating dir %s', dir)
            os.makedirs(dir)
            os.makedirs(dir + 'photos')
        else:
            self.log.info('Directory %s already exists', dir)
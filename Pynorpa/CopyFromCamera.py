"""
 Copy JPG images from Nikon D800 camera.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import datetime
import glob
import os
#import config
import logging
from PIL import Image, ExifTags
from Timer import *


class CopyFromCamera:
    """Copy JPG images from Nikon D800 camera."""
    log = logging.getLogger(__name__)

    def __init__(self):
        """Constructor."""
        self.log.info('Constructor')
        self.images = []
        self.sourceDir = None
        self.targetDir = None

    def loadImages(self):
        """Load the list of images to copy."""

        # Find source and target directories
        self.sourceDir = self.getCameraDir()
        self.targetDir = self.getCurrentTarget()
        if not os.path.exists(self.sourceDir):
            self.log.error('Camera is not mounted at %s !', self.sourceDir)
            return
        else:
            self.log.info('Camera is mounted at %s', self.sourceDir)
        self.createNatureDirs(self.targetDir)

        # Glob images
        self.images = sorted(glob.glob(self.sourceDir + '*.JPG'))
        self.log.info('Found %d images', len(self.images))

    def copyImages(self):
        """Copy JPG images from the mounted camera."""
        if len(self.images) == 0:
            return
        timer = Timer()
        self.log.info('Copying images from %s to %s', self.sourceDir, self.targetDir)
        for img in self.images:
            self.identify(img)
            #dest = f'{self.targetDir}orig/{os.path.basename(img)}'
            dest = f'{self.targetDir}orig/'
            cmd = 'cp ' + img.replace(" ", "\\ ") + ' ' + dest
            #self.log.info(cmd)
            os.system(cmd)
        timer.stop()
        self.log.info('Copied %d photos in %s', len(self.images), timer.getElapsed())

    def isCameraMounted(self):
        """Check if the camera is mounted."""
        if self.sourceDir is None:
            self.log.error('Camera dir is undefined!')
            return False
        return os.path.exists(self.sourceDir)
    
    def getNumberImages(self):
        """Get the number of photos to copy."""
        return len(self.images)

    def identify(self, img: str):
        """Find details like size and datetime about the specified image file."""
        im = Image.open(img)
        width, height = im.size

        # Read EXIF data
        sDateTime = 'unknown'
        exif = im.getexif()
        if exif is None:
            self.log.error('Image has no EXIF data.')
        else:
            #self.log.info('  shot at %s', exif[ExifTags.Base.DateTime])
            for key, val in exif.items():
                if key in ExifTags.TAGS and ExifTags.TAGS[key] == 'DateTime':
                    #print(f'tag {ExifTags.TAGS[key]}:{val}')
                    sDateTime = val
        self.log.info('Copying %s size %dx%dpx shot at %s', os.path.basename(img), width, height, sDateTime)

    def getCameraDir(self):
        """Get the current photo dir on the mounted camera."""
        # TODO increment past 105
        dir = r'/media/nicz/NIKON D800/DCIM/105ND800/'
        return dir

    def getCurrentTarget(self):
        """Get current target image directory. Name is based on year and month."""
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        year = date.strftime("%Y")
        month = date.strftime("%m")
        dir = f'/home/nicz/Pictures/Nature-{year}-{month}/'
        return dir
    
    def createNatureDirs(self, dir):
        """Create photo directories if needed."""
        if not os.path.exists(dir):
            self.log.info('Creating dir %s', dir)
            os.makedirs(dir)
            os.makedirs(dir + 'orig')
            os.makedirs(dir + 'photos')
            os.makedirs(dir + 'thumbs')
            os.makedirs(dir + 'geotracker')
        else:
            self.log.info('Directory %s already exists', dir)
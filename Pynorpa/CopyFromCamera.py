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

    def copyImages(self):
        """Copy JPG images from the mounted camera."""
        timer = Timer()

        # Find source and target directories
        sourceDir = self.getCameraDir()
        if not os.path.exists(sourceDir):
            self.log.error('Camera is not mounted at %s !', sourceDir)
            exit()

        targetDir = self.getCurrentTarget()
        self.createNatureDirs(targetDir)
        self.log.info('Copying images from %s to %s', sourceDir, targetDir)

        # Glob images
        images = sorted(glob.glob(sourceDir + '*.JPG'))
        self.log.info('Found %d images', len(images))
        for img in images:
            self.identify(img)
            dest = f'{targetDir}orig/{os.path.basename(img)}'
            os.system(f'cp {img} {dest}')
        timer.stop()
        self.log.info('Copied %d photos in %s', len(images), timer.getElapsed())

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
        # TODO /home/nicz/Pictures/
        dir = f'Nature-{year}-{month}/'
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
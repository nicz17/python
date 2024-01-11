"""
 Container class for an image file
 with filename, size, and relevant EXIF tags.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import glob
import exifread
from PIL import Image, ExifTags

class PhotoInfo:
    log = logging.getLogger(__name__)

    def __init__(self, filename: str):
        """Constructor from full filename."""
        self.log.info('Constructor from %s', filename)
        self.filename = filename
        self.shotat = None
        self.width  = None
        self.height = None

    def identify(self):
        """Find details like size and shot-at about this image file."""
        img = Image.open(self.filename)
        self.width, self.height = img.size

        # Read EXIF data
        exif = img.getexif()
        if exif is None:
            self.log.error('Image has no EXIF data.')
        else:
            for key, val in exif.items():
                if key in ExifTags.TAGS and ExifTags.TAGS[key] == 'DateTime':
                    self.shotat = val

    def listAllExif(self):
        """List all existing EXIF tags."""
        img = Image.open(self.filename)
        exif = img.getexif()
        if exif is None:
            self.log.error('Image has no EXIF data.')
        else:
            self.log.info('Found %d EXIF tags:', len(exif.items()))
            for key, val in exif.items():
                if key in ExifTags.TAGS:
                    self.log.info('Tag %s : %s', ExifTags.TAGS[key], val)

    def listExifread(self):
        file = open(self.filename, 'rb')
        tags = exifread.process_file(file)
        for tag in tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                self.log.info('Tag %s : %s', tag, tags[tag])
            else:
                self.log.info('Skipping tag %s', tag)
                    
    def __str__(self):
        str = f'PhotoInfo {self.filename} [{self.width}x{self.height}] {self.shotat}'
        return str
    
def testPhotoInfo():
    dir = '/home/nicz/Pictures/Nature-2023-12/photos/'
    images = sorted(glob.glob(dir + '*.jpg'))
    for img in images:
        info = PhotoInfo(img)
        #info.listAllExif()
        info.listExifread()

if __name__ == '__main__':
    logging.basicConfig(format="[%(levelname)s] %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testPhotoInfo()
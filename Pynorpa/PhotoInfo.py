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

class PhotoInfo:
    log = logging.getLogger(__name__)

    def __init__(self, filename: str):
        """Constructor from full filename."""
        self.log.info('Constructor from %s', filename)
        self.filename = filename
        self.shotat = None
        self.width  = None
        self.height = None
        self.lat = None
        self.lon = None

    def identify(self):
        """Load details like size and shot-at from this image's EXIF tags."""
        file = open(self.filename, 'rb')
        tags = exifread.process_file(file, details=False)
        for tag in tags.keys():
            if tag == 'EXIF DateTimeOriginal':
                self.shotat = tags[tag]
            elif tag == 'EXIF ExifImageWidth':
                self.width = tags[tag]
            elif tag == 'EXIF ExifImageLength':
                self.height = tags[tag]
        gpsCoords = exifread.utils.get_gps_coords(tags)
        if gpsCoords:
            self.lat, self.lon = gpsCoords
        file.close()
        self.log.debug(self)

    def listAllExif(self):
        """List all existing EXIF tags."""
        file = open(self.filename, 'rb')
        tags = exifread.process_file(file)
        for tag in tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                self.log.info('Tag %s : %s', tag, tags[tag])
            else:
                self.log.info('Skipping tag %s', tag)
        file.close()
                    
    def __str__(self):
        str = f'PhotoInfo {self.filename} [{self.width}x{self.height}] {self.shotat} Lon/Lat {self.lon}/{self.lat}'
        return str
    
def testPhotoInfo():
    dir = '/home/nicz/Pictures/Nature-2023-12/photos/'
    files = sorted(glob.glob(dir + '*.jpg'))
    photos = []
    for file in files:
        photo = PhotoInfo(file)
        #info.listAllExif()
        photo.identify()
        photo.log.info(photo)
        photos.append(photo)
    print(f'Found {len(photos)} photos from {photos[0].shotat} to {photos[-1].shotat}')

if __name__ == '__main__':
    logging.basicConfig(format="[%(levelname)s] %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testPhotoInfo()
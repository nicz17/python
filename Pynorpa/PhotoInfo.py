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
import os
import DateTools
from LocationCache import Location

class PhotoInfo:
    log = logging.getLogger(__name__)

    def __init__(self, filename: str):
        """Constructor from full filename."""
        self.log.debug('Constructor from %s', filename)
        self.filename = filename
        self.tShotAt = None
        self.width  = None
        self.height = None
        self.lat = None
        self.lon = None
        self.focalLength = None
        self.exposureTime = None
        self.fNumber = None
        self.isoRating = None
        self.closeTo = None

    def getNameShort(self) -> str:
        """Get the base file name of this photo."""
        return os.path.basename(self.filename)

    def getNameFull(self) -> str:
        """Get the full file name of this photo."""
        return self.filename
    
    def getShotAtString(self) -> str:
        """Get the shot-at timestamp of this photo as a string."""
        return DateTools.timestampToString(self.tShotAt)
    
    def getShotAt(self) -> float:
        """Get the shot-at timestamp of this photo as a float."""
        return self.tShotAt
    
    def getSizeString(self) -> str:
        """Get the size as width x height string, in pixels."""
        return f'{self.width}x{self.height} px'
    
    def getGPSString(self) -> str:
        """Get GPS data as string."""
        if self.hasGPSData():
            return f'GPS {self.lon:.6f}/{self.lat:.6f}'
        else:
            return 'No GPS data'
        
    def getCloseTo(self) -> str:
        """Get closest known location."""
        return self.closeTo if self.closeTo else 'Inconnu'
    
    def setCloseTo(self, location: Location):
        if location:
            self.closeTo = location.getName()

    def identify(self):
        """Load details like size, shot-at and GPS from this image's EXIF tags."""
        file = open(self.filename, 'rb')
        tags = exifread.process_file(file, details=False)
        for tag in tags.keys():
            if tag == 'EXIF DateTimeOriginal':
                self.tShotAt = DateTools.exifToTimestamp(str(tags[tag]))
                self.log.debug('Shot at timestamp %f: %s', self.tShotAt, DateTools.timestampToString(self.tShotAt))
            elif tag == 'EXIF ExifImageWidth':
                self.width = tags[tag]
            elif tag == 'EXIF ExifImageLength':
                self.height = tags[tag]
            elif tag == 'EXIF FocalLength':
                self.focalLength = tags[tag]
            elif tag == 'EXIF ExposureTime':
                self.exposureTime = tags[tag]
            elif tag == 'EXIF FNumber':
                self.fNumber = tags[tag]
            elif tag == 'EXIF ISOSpeedRatings':
                self.isoRating = tags[tag]
        gpsCoords = exifread.utils.get_gps_coords(tags)
        if gpsCoords:
            self.lat, self.lon = gpsCoords
        file.close()
        self.log.debug(self)

    def hasGPSData(self) -> bool:
        """Checks if this photo has GPS EXIF tags defined."""
        return self.lat is not None and self.lon is not None
    
    def getExposureDetails(self) -> str:
        """Gets exposure info, for example 400mm f/32 1/200s ISO 200"""
        return f'{self.focalLength}mm f/{self.fNumber} {self.exposureTime}s ISO {self.isoRating}'

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
        str  = f'PhotoInfo {self.filename} [{self.width}x{self.height}] '
        str += f'{DateTools.timestampToString(self.tShotAt)} Lon/Lat {self.lon}/{self.lat}'
        return str
    
def testPhotoInfo():
    dir = '/home/nicz/Pictures/Nature-2023-12/photos/'
    files = sorted(glob.glob(dir + '*.jpg'))
    photos = []
    for file in files:
        photo = PhotoInfo(file)
        photo.listAllExif()
        photo.identify()
        photo.log.info(photo)
        photos.append(photo)
    sStart = DateTools.timestampToString(photos[0].tShotAt)
    sEnd   = DateTools.timestampToString(photos[-1].tShotAt)
    print(f'Found {len(photos)} photos from {sStart} to {sEnd}')

if __name__ == '__main__':
    logging.basicConfig(format="[%(levelname)s] %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testPhotoInfo()
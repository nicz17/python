"""
 Copy GPX GeoTracking files and apply GPS coords to photos.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import datetime
import glob
import gpxpy
import gpxpy.gpx
#import config
import logging
import os
from PIL import Image, ExifTags
from Timer import *


class GeoTracker:
    """Copy GPX GeoTracking files and apply GPS coords to photos."""
    log = logging.getLogger('GeoTracker')
    dirSource = '/home/nicz/Dropbox/GeoTrack/'
    dirTarget = None

    def __init__(self):
        """Constructor."""
        self.log.info('Constructor')
        self.getTargetDirectory()
        self.files = []

    def prepare(self):
        """Check source and target dirs, list photos to update."""

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
        self.files = sorted(glob.glob(filter))
        self.log.info('Found %d GeoTrack files in %s', len(self.files), filter)

    def copyFiles(self):
        """Copy GPX GeoTrack files from DropBox."""

        # Copy files
        for file in self.files:
            self.log.info('Copying %s', os.path.basename(file))
            dest = self.dirTarget + os.path.basename(file)
            os.system(f'cp {file} {dest}')

    def loadGeoTracks(self):
        """Load the GPX data from our .gpx files."""
        filter = self.dirTarget + '*.gpx'
        files = sorted(glob.glob(filter))
        for file in files:
            track = GeoTrack(file)
            track.loadData()

    def getTargetDirectory(self):
        """Build target directory name from current date."""
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        year  = date.strftime("%Y")
        month = date.strftime("%m")
        self.dirTarget = f'/home/nicz/Pictures/Nature-{year}-{month}/geotracker/'
        self.log.info('Target directory is %s', self.dirTarget)
        
class GeoTrack:
    """Read a .gpx file and store the track."""
    log = logging.getLogger('GeoTrack')

    def __init__(self, filename) -> None:
        """Constructor from file name. Does not read the file."""
        self.log.info('Constructor from %s', filename)
        self.filename = filename
        self.name = os.path.basename(filename)

    def loadData(self):
        """Open and parse the GPX file."""
        gpxFile = open(self.filename, 'r')
        gpx = gpxpy.parse(gpxFile)
        gpxFile.close()

        if gpx.name is not None:
            self.name = gpx.name
        tStart, tEnd = gpx.get_time_bounds()

        self.log.info('GPX %s has %d tracks, from %s to %s', gpx.name, len(gpx.tracks), tStart, tEnd)
        for track in gpx.tracks:
            self.log.info('Track has %d segments', len(track.segments))
            for segment in track.segments:
                self.log.info('Segment has %d points', len(segment.points))
                for point in segment.points:
                    pass
                    #self.log.info(f'Point at ({point.latitude},{point.longitude}) -> {point.elevation}m {point.time}')
                
    def getLocationAt(self, tAt: float):
        """Get the GPS coordinates for the specified timestamp."""
        # TODO use self.gpx.get_location_at(tAt)
        pass

    def __str__(self) -> str:
        str = f'GeoTrack {self.filename}'
        return str
    
def testGeoTracker():
    tracker = GeoTracker()
    tracker.prepare()
    tracker.loadGeoTracks()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testGeoTracker()
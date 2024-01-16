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
import config
import logging
import os
import DateTools
from Timer import *


class GeoTracker:
    """Copy GPX GeoTracking files and apply GPS coords to photos."""
    log = logging.getLogger('GeoTracker')
    dirSource = config.dirSourceGeoTrack
    dirTarget = None

    def __init__(self):
        """Constructor."""
        self.log.info('Constructor')
        self.getTargetDirectory()
        self.files = []
        self.geoTracks = []

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
            self.geoTracks.append(track)
            tAt = 1705069208.0
            dtAt = DateTools.timestampToDatetimeUTC(tAt)
            loc = track.getLocationAt(dtAt)
            self.log.info('Location is %s', loc)

    def getTargetDirectory(self):
        """Build target directory name from current date."""
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        year  = date.strftime("%Y")
        month = date.strftime("%m")
        self.dirTarget = f'{config.dirPhotosBase}Nature-{year}-{month}/geotracker/'
        self.log.info('Target directory is %s', self.dirTarget)
        
class GeoTrack:
    """Read a .gpx file and store the track."""
    log = logging.getLogger('GeoTrack')

    def __init__(self, filename) -> None:
        """Constructor from file name. Does not read the file."""
        self.log.info('Constructor from %s', filename)
        self.filename = filename
        self.name = os.path.basename(filename)
        self.gpx = None
        self.tStart = None
        self.tEnd   = None
        self.meanLon = None
        self.meanLat = None

    def loadData(self):
        """Open and parse the GPX file."""
        gpxFile = open(self.filename, 'r')
        self.gpx = gpxpy.parse(gpxFile)
        gpxFile.close()

        if self.gpx.name is not None:
            self.name = self.gpx.name
        self.tStart, self.tEnd = self.gpx.get_time_bounds()

        # Build stats for center point
        nPoints = 0
        sumLon = 0.0
        sumLat = 0.0

        self.log.info('GPX %s has %d tracks, from %s to %s', self.gpx.name, 
                      len(self.gpx.tracks), self.tStart, self.tEnd)
        for track in self.gpx.tracks:
            self.log.info('Track has %d segments', len(track.segments))
            for segment in track.segments:
                self.log.info('Segment has %d points', len(segment.points))
                nPoints += len(segment.points)
                for point in segment.points:
                    sumLon += point.longitude
                    sumLat += point.latitude
                    #self.log.info(f'Point at ({point.latitude},{point.longitude}) -> {point.elevation}m {point.time}')

        # Center point
        if nPoints > 0:
            self.meanLon = sumLon/nPoints
            self.meanLat = sumLat/nPoints
        self.log.info('Track center point is %f/%f', self.meanLat, self.meanLon)
                
    def getLocationAt(self, dtAt: datetime.datetime):
        """Get the GPS coordinates for the specified timestamp."""
        if self.gpx is None:
            self.log.error('GPX data is not loaded')
            return None
        self.log.info('Getting location at %s', dtAt)
        if self.contains(dtAt):
            return self.gpx.get_location_at(dtAt)
        else:
            self.log.info('Timestamp %s is out of bounds', dtAt)
            return None
        
    def getCenter(self):
        """Return the central point of this track as a float lat/lon pair."""
        return self.meanLat, self.meanLon
        
    def contains(self, dtAt: datetime.datetime) -> bool:
        """Check if the specified datetime is contained in this track's daterange."""
        if self.gpx is None:
            self.log.error('GPX data not loaded!')
            return False
        dtStart, dtEnd = self.gpx.get_time_bounds()
        return (dtAt >= dtStart and dtAt <= dtEnd)

    def __str__(self) -> str:
        str = f'GeoTrack {self.name}'
        return str
    
def testGeoTracker():
    tracker = GeoTracker()
    tracker.prepare()
    tracker.loadGeoTracks()
    # TODO test with tAt = 1705066208.0
    

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testGeoTracker()
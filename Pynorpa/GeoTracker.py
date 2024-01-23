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
import gpxpy.geo
import config
import logging
import os
import DateTools
from Timer import *
from LocationCache import *
from PhotoInfo import *


class GeoTracker:
    """Copy GPX GeoTracking files and apply GPS coords to photos."""
    log = logging.getLogger('GeoTracker')
    dirSource = config.dirSourceGeoTrack
    dirTarget = None
    dirPhotos = None

    def __init__(self):
        """Constructor."""
        self.log.info('Constructor')
        self.getTargetDirectory()
        self.files = []
        self.geoTracks = []
        self.locationCache = None

    def prepare(self):
        """Check source and target dirs, list photos to update."""

        # Check dirs exist
        if not os.path.exists(self.dirTarget):
            self.log.error('Missing target dir %s', self.dirTarget)
            return
        if not os.path.exists(self.dirPhotos):
            self.log.error('Missing photos dir %s', self.dirPhotos)
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

        # Load LocationCache
        self.locationCache = LocationCache()
        self.locationCache.load()

    def copyFiles(self):
        """Copy GPX GeoTrack files from DropBox."""
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
            loc = self.locationCache.getClosest(track.center.latitude, track.center.longitude)
            self.log.info('Closest location in cache to track %s is %s', track.name, loc)

    def getLocationAt(self, tAt: float):
        """Get the GPS coordinates for the specified UNIX timestamp."""
        dtAt = DateTools.timestampToDatetimeUTC(tAt)
        for track in self.geoTracks:
            gpxloc = track.getLocationAt(dtAt)
            if gpxloc is not None:
                self.log.info('Location in %s is %s', track.name, gpxloc)
                dist = gpxloc.distance_2d(track.center)
                self.log.info('Distance to center %fm', dist)
                loc = self.locationCache.getClosest(gpxloc.latitude, gpxloc.longitude)
                self.log.info('Closest location in cache is %s', loc)
                return gpxloc
            
    def setPhotoGPSTags(self):
        """Get newly uploaded photos and add GPS EXIF tags if possible."""
        #filter = self.dirPhotos + '*.JPG'
        filter = 'Nature-2024-01/orig/*0.JPG' # TODO remove test
        files = sorted(glob.glob(filter))
        self.log.info('Looking for photos in %s', filter)
        self.log.info('Will try to update %d photos with GPS tags', len(files))
        nUpdated = 0
        for file in files:
            photo = PhotoInfo(file)
            photo.identify()
            if photo.hasGPSData():
                self.log.info('%s already has GPS data', photo)
            else:
                self.log.info('Adding GPS data to %s', photo)
                gpxloc = self.getLocationAt(photo.tShotAt)
                if self.callExifTool(file, gpxloc):
                    nUpdated += 1
        self.log.info('Updated %d photos with GPS tags', nUpdated)

    def callExifTool(self, file: str, gpxloc: gpxpy.geo.Location):
        """Set EXIF GPS tags from gpxloc using exiftool."""
        if gpxloc is None:
            self.log.error('Undefined GPX location for exiftool')
            return False
        # exiftool -GPSLatitude*=40.6892 -GPSLongitude*=-74.0445 -GPSAltitude*=10 FILE
        cmd = f'exiftool -GPSLatitude*={gpxloc.latitude} -GPSLongitude*={gpxloc.longitude} {file}'
        self.log.debug(cmd)
        os.system(cmd)
        return True

    def getTargetDirectory(self):
        """Build target directory name from current date."""
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        year  = date.strftime("%Y")
        month = date.strftime("%m")
        self.dirTarget = f'{config.dirPhotosBase}Nature-{year}-{month}/geotracker/'
        self.dirPhotos = f'{config.dirPhotosBase}Nature-{year}-{month}/orig/'
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
        self.center = None

    def loadData(self):
        """Open and parse the GPX file. Computes the center point."""
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
            meanLon = sumLon/nPoints
            meanLat = sumLat/nPoints
            self.center = gpxpy.geo.Location(meanLat, meanLon)
        self.log.info('Track center point is %s', self.center)
                
    def getLocationAt(self, dtAt: datetime.datetime) -> gpxpy.geo.Location:
        """Get the GPS coordinates for the specified timestamp."""
        if self.gpx is None:
            self.log.error('GPX data is not loaded')
            return None
        self.log.info('Getting location at %s', dtAt)
        if self.contains(dtAt):
            locs = self.gpx.get_location_at(dtAt)
            if locs is not None and len(locs) > 0:
                return locs[0]
            else:
                return None
        else:
            self.log.info('Timestamp %s is out of bounds for %s', dtAt, self)
            return None
        
    def getCenter(self) -> gpxpy.geo.Location:
        """Return the central point of this track as a gpxpy.geo.Location."""
        return self.center
        
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
    tracker.setPhotoGPSTags()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testGeoTracker()
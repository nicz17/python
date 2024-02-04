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
from HtmlPage import *
from Timer import *
from LocationCache import *
from PhotoInfo import *
#from GeoTrackHtmlPage import *


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
        self.photos = []

    def prepare(self):
        """Check source and target dirs, list photos to update, load LocationCache."""

        # Load LocationCache
        self.locationCache = LocationCache()
        self.locationCache.load()

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
        filter = self.dirPhotos + '*.JPG'
        #filter = 'Nature-2024-01/orig/*0.JPG' # TODO remove test
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
                    photo.identify()
            self.photos.append(photo)
        self.log.info('Updated %d photos with GPS tags', nUpdated)

    def callExifTool(self, file: str, gpxloc: gpxpy.geo.Location):
        """Set EXIF GPS tags from gpxloc using exiftool."""
        if gpxloc is None:
            self.log.error('Undefined GPX location for exiftool for %s', file)
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
        #self.dirTarget = f'{config.dirPhotosBase}Nature-2024-01/geotracker/'  # TODO remove test
        self.log.info('Target directory is %s', self.dirTarget)

    def buildHtmlPreviews(self):
        """Build HTML preview pages for each GeoTrack."""
        track: GeoTrack
        for track in self.geoTracks:
            loc = self.locationCache.getClosest(track.center.latitude, track.center.longitude)
            page = GeoTrackHtmlPage(track.name)
            page.build(track, self.photos, loc)
            page.save(f'{self.dirTarget}track{track.name}.html')
        
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


class GeoTrackHtmlPage(HtmlPage):
    log = logging.getLogger('GeoTrackHtmlPage')

    def __init__(self, sTitle: str):
        """Constructor with title."""
        super().__init__(sTitle, 'http://www.tf79.ch/nature/style.css')
        self.head.addTag(HtmlComment('Generated by pynorpa.py on ' + DateTools.nowAsString()))
        self.head.addTag(MetaHtmlTag('author', 'Nicolas Zwahlen'))
        self.includeScript('http://www.tf79.ch/nature/js/OpenLayers-v5.3.0.js')
        self.includeScript('http://www.tf79.ch/nature/js/panorpa-maps.js')
        self.addCssLink('http://www.tf79.ch/nature/css/OpenLayers-v5.3.0.css')

    def build(self, track: GeoTrack, photos, location: Location):
        """Build page content from the specified GeoTrack."""
        self.log.info('Building preview of %s with %d photos', track.name, len(photos))
        self.addHeading(1, f'Preview of GeoTrack {track.name}')

        # OpenLayers map
        divPopup = DivHtmlTag('ol-popup')
        divMap = DivHtmlTag('ol-map', 'ol-map')
        divMap.addTag(divPopup)

        # GeoTrack info div
        aTrackInfo = []
        aTrackInfo.append('Name: ' + track.name)
        aTrackInfo.append(DateTools.datetimeToString(track.tStart) + ' - ' + DateTools.datetimeToString(track.tEnd))
        aTrackInfo.append(f'Photos: {len(photos)}')
        if location is not None:
            aTrackInfo.append(f'Closest location: {location.name}')
        divTrackInfo = MyBoxHtmlTag('GeoTrack details')
        divTrackInfo.addTag(ListHtmlTag(aTrackInfo))

        # Table with map and info boxes
        table = TableHtmlTag([divMap, divTrackInfo], 2)
        table.addAttr('class', 'align-top').addAttr('width', '1440px')
        self.main.addTag(table)

        # JS script with map items
        js  = '\n\tvar oVectorSource, oIconStyle;\n'
        js += f'\trenderMap({track.center.longitude:.6f}, {track.center.latitude:.6f}, 16);\n'
        js += f'\taddMapMarker({track.center.longitude:.6f}, {track.center.latitude:.6f}, "Track center");\n'
        if location is not None:
            js += f'\taddMapMarker({location.lon:.6f}, {location.lat:.6f}, "{location.name}");\n'
        photo: PhotoInfo
        for photo in photos:
            if photo.hasGPSData():
                js += f'\taddPicMarker({photo.lon:.6f}, {photo.lat:.6f}, "{photo.filename}", "");\n'
            else:
                self.log.info('No GPS data in %s', photo.filename)
        self.main.addTag(ScriptHtmlTag(js))

    def buildMenu(self):
        """Build the left-hand side menu with links."""
        self.menu = DivHtmlTag('menu')
        self.body.addTag(self.menu)
        self.menu.addTag(HtmlTag('h1', '<a href="#">Local preview</a>'))
        self.menu.addTag(HtmlTag('h3', '<a href="http://www.tf79.ch/index.html">TF79.ch</a>'))
        self.menu.addTag(HtmlTag('h3', '<a href="http://www.tf79.ch/nature/">Nature</a>'))


def testGeoTracker():
    tracker = GeoTracker()
    tracker.prepare()
    tracker.loadGeoTracks()
    tracker.setPhotoGPSTags()
    tracker.buildHtmlPreviews()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testGeoTracker()
"""
 Subclasses of Task for Pynorpa app.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import config
import time
import TextTools
from Task import *
from CopyFromCamera import *
from GeoTracker import *

class PynorpaTask(Task):
    log = logging.getLogger(__name__)

    def __init__(self, title: str, desc: str, nStepsTotal: int):
        super().__init__(title, desc, nStepsTotal)
        self.tStart = None
        self.tEnd   = None

    def prepare(self):
        """Prepare this task. Must be done before running."""
        pass

    def run(self):
        """Run this task."""
        self.tStart = time.time()
        self.log.info('Running')

    def onDone(self):
        if not self.tEnd:
            self.tEnd = time.time()

    def getStatus(self) -> str:
        sLeft = self.getRemainingTime()
        return f'{self.status} [{self.nStepsDone}/{self.nStepsTotal}] {sLeft}'
    
    def getRemainingTime(self):
        """Estimate the remaining time."""
        result = ''
        nTotal = self.nStepsTotal
        nDone  = self.nStepsDone
        if self.tStart and nTotal and nDone and nTotal > 0 and nDone > 0:
            if nDone < nTotal:
                tUsed = time.time() - self.tStart
                tLeft = (nTotal - nDone)*tUsed/nDone
                result = f'{TextTools.durationToString(tLeft)} remaining'
            elif nDone >= nTotal and self.tEnd:
                tUsed = self.tEnd - self.tStart
                result = f'in {TextTools.durationToString(tUsed)}'
        return result


class MountCameraTask(PynorpaTask):
    """Just check that the camera is mounted."""
    log = logging.getLogger('MountCameraTask')

    def __init__(self, copier: CopyFromCamera, cbkUpdate = None):
        super().__init__('Mount Camera', 'Mount camera memory card', 1)
        self.copier = copier
        self.cbkUpdate = cbkUpdate

    def prepare(self):
        self.log.info('Prepare')
        self.copier.getCameraDir()

    def run(self):
        super().run()
        if self.copier.isCameraMounted():
            self.inc()
            self.setDesc(f'Camera is mounted at {self.copier.getCameraDir()}')
        else:
            self.setDesc(f'Camera is not mounted at {config.dirCameraBase}')
            self.setStatus('Error')
        self.cbkUpdate()

class CreateThumbnailsTask(PynorpaTask):
    """Create miniatures for copied photos."""
    log = logging.getLogger('CreateThumbnailsTask')

    def __init__(self, copier: CopyFromCamera, cbkUpdate):
        super().__init__('Create previews', 'Create previews for copied photos', copier.getNumberImages())
        self.copier = copier
        self.cbkUpdate = cbkUpdate

    def prepare(self):
        self.log.info('Prepare')
        self.setDesc(self.copier.getStatusMessage())

    def run(self):
        super().run()
        self.copier.createThumbs(self.onProgress)
        self.setDesc(self.copier.getStatusMessage())
        self.cbkUpdate()

    def onProgress(self):
        self.inc()
        self.setDesc(self.copier.getStatusMessage())
        self.cbkUpdate()

class CopyFromCameraTask(PynorpaTask):
    """Copy pictures from camera memory card."""
    log = logging.getLogger('CopyFromCameraTask')

    def __init__(self, copier: CopyFromCamera, cbkUpdate):
        super().__init__('Copy photos', 'Copy pictures from camera memory card', copier.getNumberImages())
        self.copier = copier
        self.cbkUpdate = cbkUpdate

    def prepare(self):
        self.log.info('Prepare')
        #self.copier.loadImages()
        self.setDesc(self.copier.getStatusMessage())

    def run(self):
        super().run()
        self.copier.copyImages(self.onProgress)
        self.setDesc(self.copier.getStatusMessage())
        self.cbkUpdate()

    def onProgress(self):
        self.inc()
        self.setDesc(self.copier.getStatusMessage())
        self.cbkUpdate()

class CopyFromDropBoxTask(PynorpaTask):
    """Copy pictures from DropBox."""
    log = logging.getLogger('CopyFromDropBoxTask')

    def __init__(self, copier: CopyFromDropBox, cbkUpdate):
        super().__init__('Copy S8 photos', 'Copy S8 pictures from DropBox', copier.getNumberImages())
        self.copier = copier
        self.cbkUpdate = cbkUpdate

    def prepare(self):
        self.log.info('Prepare')
        self.setDesc(self.copier.getStatusMessage())

    def run(self):
        super().run()
        self.copier.copyImages(self.onProgress)
        self.setDesc(self.copier.getStatusMessage())
        self.cbkUpdate()

    def onProgress(self):
        self.inc()
        self.setDesc(self.copier.getStatusMessage())
        self.cbkUpdate()

class GeoTrackerTask(PynorpaTask):
    """Add GPS tags to copied pictures."""
    log = logging.getLogger('GeoTrackerTask')

    def __init__(self, tracker: GeoTracker, nPhotos: int, cbkUpdate):
        super().__init__('Geotracking', 'Add GPS tags to copied photos', nPhotos)
        self.tracker = tracker
        self.cbkUpdate = cbkUpdate

    def prepare(self):
        self.log.info('Prepare')
        self.tracker.copyFiles()
        self.setDesc(self.tracker.getStatusMessage())

    def run(self):
        super().run()
        self.tracker.loadGeoTracks()
        self.tracker.loadPhotos()
        self.setDesc(self.tracker.getStatusMessage())
        self.cbkUpdate()
        self.tracker.setPhotoGPSTags(self.onProgress)
        self.setDesc(self.tracker.getStatusMessage())
        self.cbkUpdate()
        #self.tracker.buildHtmlPreviews()

    def onProgress(self):
        if not self.isOver():
            self.inc()
        self.setDesc(self.tracker.getStatusMessage())
        self.cbkUpdate()

class TestMapView(PynorpaTask):
    """Test map widget interactions with static GeoTrack."""
    log = logging.getLogger('TestMapView')

    def __init__(self, cbkCenterMap, cbkBoundinBox, cbkAddMarker):
        super().__init__('Test map view', 'Test map with known GeoTrack', 10)
        self.track = None
        self.cbkCenterMap = cbkCenterMap
        self.cbkBoundinBox = cbkBoundinBox
        self.cbkAddMarker  = cbkAddMarker

    def prepare(self):
        self.log.info('Prepare')
        self.track = GeoTrack('Nature-2024-01/geotracker/Sorge240112.gpx')
        self.setDesc(self.track.name)
        self.jpgFiles = sorted(glob.glob('Nature-2024-01/orig/*.JPG'))

    def run(self):
        super().run()
        self.track.loadData()

        # Set map center
        center = self.track.getCenter()
        if center:
            llzCenter = LatLonZoom(center.latitude, center.longitude, 14)
            self.cbkCenterMap(llzCenter)
            self.inc()
        else:
            self.setDesc('Failed to find center!')

        # Set map bounding box
        self.cbkBoundinBox(*self.track.bbox)
        self.inc()

        # Add map markers
        for file in self.jpgFiles:
            photo = PhotoInfo(file)
            photo.identify()
            if photo.hasGPSData():
                self.cbkAddMarker(photo.lat, photo.lon, 'resources/location-pic.png')
                self.inc()


class TestPynorpaTask(PynorpaTask):
    """Test with sleeping steps."""
    log = logging.getLogger('TestPynorpaTask')

    def __init__(self, steps: int, cbkUpdate):
        """Constructor with number of 1-second steps."""
        self.nSteps = steps
        self.cbkUpdate = cbkUpdate
        super().__init__('Test case', f'Sleep {steps} times then move on', steps)

    def prepare(self):
        self.log.info('Prepare')
        self.setDesc('Sleepy!')

    def run(self):
        super().run()
        for iStep in range(self.nSteps):
            self.log.info('Sleeping %d/%d', iStep, self.nSteps)
            self.setDesc(f'Power nap {iStep+1} in progress')
            if self.cbkUpdate:
                self.cbkUpdate()
            time.sleep(1)
            self.inc()
        self.setDesc('Slept well.')
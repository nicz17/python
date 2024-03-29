"""
 Subclasses of Task for Pynorpa app.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import config
import time
from Task import *
from CopyFromCamera import *
from GeoTracker import *

class PynorpaTask(Task):
    log = logging.getLogger(__name__)

    def __init__(self, title: str, desc: str, nStepsTotal: int):
        super().__init__(title, desc, nStepsTotal)

    def prepare(self):
        """Prepare this task. Must be done before running."""
        pass

    def run(self):
        """Run this task."""
        pass

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
        self.log.info('Running')
        if self.copier.isCameraMounted():
            self.inc()
            self.setDesc(f'Camera is mounted at {self.copier.getCameraDir()}')
        else:
            self.setDesc(f'Camera is not mounted at {config.dirCameraBase}')
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
        self.log.info('Running')
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
        self.copier.loadImages()
        self.setDesc(self.copier.getStatusMessage())

    def run(self):
        self.log.info('Running')
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

    def __init__(self, tracker: GeoTracker, cbkUpdate):
        super().__init__('Geotracking', 'Add GPS tags to copied photos', tracker.getNumberImages())
        self.tracker = tracker
        self.cbkUpdate = cbkUpdate

    def prepare(self):
        self.log.info('Prepare')
        #self.tracker.prepare()  TODO must be done before constructor... reset nTasks here
        self.tracker.copyFiles()
        self.setDesc(self.tracker.getStatusMessage())

    def run(self):
        self.log.info('Running')
        self.tracker.loadGeoTracks()
        self.setDesc(self.tracker.getStatusMessage())
        self.cbkUpdate()
        self.tracker.setPhotoGPSTags(self.onProgress)
        self.setDesc(self.tracker.getStatusMessage())
        self.cbkUpdate()
        self.tracker.buildHtmlPreviews() # TODO move to own task ?

    def onProgress(self):
        self.inc()
        self.setDesc(self.tracker.getStatusMessage())
        self.cbkUpdate()


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
        self.log.info('Running')
        for iStep in range(self.nSteps):
            self.log.info('Sleeping %d/%d', iStep, self.nSteps)
            self.setDesc(f'Power nap {iStep+1} in progress')
            if self.cbkUpdate:
                self.cbkUpdate()
            time.sleep(1)
            self.inc()
        self.setDesc('Slept well.')
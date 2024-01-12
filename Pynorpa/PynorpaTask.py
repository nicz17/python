"""
 Subclasses of Task for Pynorpa app.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
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

    def __init__(self, copier: CopyFromCamera):
        super().__init__('Mount Camera', 'Mount camera memory card', 1)
        self.copier = copier

    def prepare(self):
        self.log.info('Prepare')
        self.copier.getCameraDir()

    def run(self):
        self.log.info('Running')
        if self.copier.isCameraMounted():
            self.inc()
            self.setDesc(f'Camera is mounted at {self.copier.getCameraDir()}')
        else:
            self.setDesc(f'Camera is not mounted at {self.copier.getCameraDir()}')

class CopyFromCameraTask(PynorpaTask):
    """Copy pictures from camera memory card."""
    log = logging.getLogger('CopyFromCameraTask')

    def __init__(self, copier: CopyFromCamera):
        super().__init__('Copy photos', 'Copy pictures from camera memory card', copier.getNumberImages())
        self.copier = copier

    def prepare(self):
        self.log.info('Prepare')
        self.copier.loadImages()

    def run(self):
        self.log.info('Running')
        self.copier.copyImages()
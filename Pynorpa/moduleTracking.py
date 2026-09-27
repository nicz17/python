"""Module for GeoTrack preview"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.0"

import config
import glob
import logging

from GeoTracker import GeoTrack
from BaseWidgets import MonthYearSelector
from MapWidget import MapWidget
from TabsApp import TabModule, TabsApp


class ModuleTracking(TabModule):
    """Class ModulePictures"""
    log = logging.getLogger('ModuleTracking')

    def __init__(self, parent: TabsApp):
        """Constructor."""
        self.window = parent.window
        self.monthYearSel = MonthYearSelector(self.loadData)
        #self.table   = TrackTable(self.onSelectTrack)
        self.mapWidget = MapWidget()
        super().__init__(parent, 'GeoTracks', GeoTrack.__name__)
        self.track = None

    def onSelectTrack(self):
        """Track selection callback."""
        pass
        # TODO display GeoTrack in mapWidget

    def loadData(self):
        """Load tracking data."""
        dir = self.getDirectory()
        self.log.info(f'Loading GeoTracks from {dir}')
        files = glob.glob(f'{dir}/*.gpx')
        for file in files:
            self.log.info(file)
        # TODO load geoTrack objects and display in table
    
    def getDirectory(self):
        """Get the geotracker dir for the selected year and month."""
        year  = self.monthYearSel.getYear()
        month = self.monthYearSel.getMonth()
        return f'{config.dirPhotosBase}Nature-{year}-{month:02d}/geotracker'

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()
        self.monthYearSel.createWidgets(self.frmLeft)
        # TODO table of GeoTracks
        self.mapWidget.createWidgets(self.frmRight)
        # TODO datetime input widget showing location on map

    def __str__(self):
        return 'ModuleTracking'
    
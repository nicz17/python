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
from BaseTable import AdvTable, TableColumn


class ModuleTracking(TabModule):
    """Class ModulePictures"""
    log = logging.getLogger('ModuleTracking')

    def __init__(self, parent: TabsApp):
        """Constructor."""
        self.window = parent.window
        self.monthYearSel = MonthYearSelector(self.loadData)
        self.table   = TableGeoTracks(self.onSelectTrack)
        self.mapWidget = MapWidget()
        super().__init__(parent, 'GeoTracks', GeoTrack.__name__)
        self.track = None

    def onSelectTrack(self, track: GeoTrack):
        """Track selection callback."""
        self.log.info(f'Selected {track}')
        bbox = track.getBoundingBox()
        if not bbox:
            track.loadData()
            bbox = track.getBoundingBox()
        self.mapWidget.setBoundingBox(bbox[0], bbox[2], bbox[1], bbox[3])

        # Display path on map
        self.mapWidget.addPath(track.getPath())


    def loadData(self):
        """Load tracking data."""
        dir = self.getDirectory()
        self.log.info(f'Loading GeoTracks from {dir}')
        files = glob.glob(f'{dir}/*.gpx')
        tracks = []
        for file in files:
            self.log.info(file)
            track = GeoTrack(file)
            tracks.append(track)
        self.table.loadData(tracks)
    
    def getDirectory(self):
        """Get the geotracker dir for the selected year and month."""
        year  = self.monthYearSel.getYear()
        month = self.monthYearSel.getMonth()
        return f'{config.dirPhotosBase}Nature-{year}-{month:02d}/geotracker'

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()
        self.monthYearSel.createWidgets(self.frmLeft)
        self.table.createWidgets(self.frmLeft)
        self.mapWidget.createWidgets(self.frmRight)
        # TODO datetime input widget showing location on map

    def __str__(self):
        return 'ModuleTracking'
    
class TableGeoTracks(AdvTable):
    """Table widget for Pynorpa GeoTracks."""
    log = logging.getLogger("TableGeoTracks")

    def __init__(self, cbkSelect):
        """Constructor with selection callback."""
        self.log.info('Constructor')
        super().__init__(cbkSelect, 'Tracks', 6)
        self.addColumn(TableColumn('Nom', GeoTrack.getNameNoExt, 400))

    def loadData(self, tracks: list[GeoTrack]):
        """Display the specified tracks in this table."""
        self.log.info('Loading %d tracks', len(tracks))
        self.clear()
        self.data = tracks
        self.addRows(tracks)


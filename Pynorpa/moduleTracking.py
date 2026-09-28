"""Module for GeoTrack preview"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.0"

import config
import glob
import logging

from tkinter import ttk

import DateTools
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
        self.table = TableGeoTracks(self.onSelectTrack)
        self.mapWidget = MapWidget()
        self.finder = PositionFinder()
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

        # Display track info in position finder
        self.finder.loadData(track)

    def loadData(self):
        """Load tracking data."""
        dir = self.getDirectory()
        self.log.info(f'Loading GeoTracks from {dir}')
        # TODO sort by start date
        files = glob.glob(f'{dir}/*.gpx')
        tracks = []
        for file in files:
            self.log.debug(file)
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
        self.finder.createWidgets(self.frmRight)
        # TODO datetime input widget showing location on map

    def __str__(self):
        return 'ModuleTracking'

class PositionFinder:
    """Helper to find the position on the track at a given time."""
    log = logging.getLogger('PositionFinder')

    def __init__(self):
        """Constructor."""
        self.track = None

    def loadData(self, track: GeoTrack):
        """Load data from the specified track."""
        self.track = track
        if track:
            start = DateTools.datetimeToString(track.getStartAt())
            end   = DateTools.datetimeToString(track.getEndAt())
            self.lblDateRange.config(text=f'{start} - {end}')
        else:
            self.lblDateRange.config(text='-')

    def createWidgets(self, parent: ttk.Frame):
        """Create user widgets."""
        self.frmMain = ttk.LabelFrame(parent, text='Positionnement')
        self.frmMain.pack(fill='x', expand=False, pady=5)
        self.lblDateRange = ttk.Label(self.frmMain, text='-')
        self.lblDateRange.pack()
        # TODO datetime input widget
        # TODO search button
        # TODO position label
    
class TableGeoTracks(AdvTable):
    """Table widget for Pynorpa GeoTracks."""
    log = logging.getLogger("TableGeoTracks")

    def __init__(self, cbkSelect):
        """Constructor with selection callback."""
        super().__init__(cbkSelect, 'Tracks', 6)
        self.addColumn(TableColumn('Nom', GeoTrack.getNameNoExt, 360))

    def loadData(self, tracks: list[GeoTrack]):
        """Display the specified tracks in this table."""
        self.log.info('Loading %d tracks', len(tracks))
        self.clear()
        self.data = tracks
        self.addRows(tracks)


"""
Tkinter map widget based on 
https://github.com/TomSchimansky/TkinterMapView
To install: pip3 install tkintermapview
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
import tkintermapview
from LocationCache import *
from LatLonZoom import *


class MapWidget():
    """A map widget."""
    log = logging.getLogger('MapWidget')
    locZero = LatLonZoom(46.5225, 6.6261, 10)

    def __init__(self):
        """Constructor"""
        self.log.info('Constructor')

    def loadData(self, location: Location):
        """Display the specified location on the map."""
        if location is not None:
            self.setLatLonZoom(location.getLatLonZoom())
        else:
            self.setDefaultLocation()

    def getLatLonZoom(self):
        """Get the current lat/lon/zoom triplet."""
        return LatLonZoom(*(self.mapView.get_position()), self.mapView.zoom)

    def setLatLonZoom(self, coords: LatLonZoom):
        """Set the map location and zoom."""
        self.mapView.set_position(coords.getLat(), coords.getLon())
        self.mapView.set_zoom(coords.getZoom())

    def addMarker(self, coords: LatLonZoom):
        """Add a marker to the map."""
        self.mapView.set_marker(coords.lat, coords.lon)
        # image = ImageTk.PhotoImage

    def setDefaultLocation(self):
        """Display the default location on the map."""
        self.setLatLonZoom(self.locZero)
        
    def createWidgets(self, parent: tk.Frame, pady=0):
        """Create user widgets."""
        self.mapView = tkintermapview.TkinterMapView(parent, width=600, height=400, corner_radius=0)
        self.mapView.pack(pady=pady)
        self.setDefaultLocation()
    
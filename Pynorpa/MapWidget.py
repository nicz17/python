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


class MapWidget():
    """A map widget."""
    log = logging.getLogger('MapWidget')
    locZero = {
        'lat': 0.0,
        'lon': 0.0,
        'zoom': 15
    }

    def __init__(self):
        """Constructor"""
        self.log.info('Constructor')

    def loadData(self, location: Location):
        """Display the specified location on the map."""
        if location is not None:
            self.mapView.set_position(location.lat, location.lon)
            self.mapView.set_zoom(location.zoom)
        else:
            self.setDefaultLocation()

    def setDefaultLocation(self):
        """Display the default location on the map."""
        self.mapView.set_position(self.locZero['lat'], self.locZero['lon'])
        self.mapView.set_zoom(self.locZero['zoom'])
        
    def createWidgets(self, parent: tk.Frame):
        """Create user widgets."""
        self.mapView = tkintermapview.TkinterMapView(parent, width=600, height=400, corner_radius=0)
        self.mapView.pack()
        self.setDefaultLocation()
    
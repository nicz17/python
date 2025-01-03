"""
Tkinter map widget based on 
https://github.com/TomSchimansky/TkinterMapView
To install: pip3 install tkintermapview
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import config
import logging
import os
import tkinter as tk
import tkintermapview
from PIL import ImageTk, Image
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

    def getZoom(self) -> int:
        """Get the current map zoom."""
        return self.mapView.zoom

    def getLatLonZoom(self) -> LatLonZoom:
        """Get the current lat/lon/zoom triplet."""
        return LatLonZoom(*(self.mapView.get_position()), self.getZoom())

    def setLatLonZoom(self, coords: LatLonZoom):
        """Set the map location and zoom."""
        self.mapView.set_position(coords.getLat(), coords.getLon())
        self.mapView.set_zoom(coords.getZoom())

    def setBoundingBox(self, latMin: float, lonMin: float, latMax: float, lonMax: float):
        """Set the map widget view to the bounding box."""
        self.mapView.fit_bounding_box((latMax, lonMin), (latMin, lonMax))

    def addMarker(self, coords: LatLonZoom, iconname=config.mapMarkerGreen):
        """Add a marker to the map."""
        if iconname and os.path.exists(iconname):
            marker = ImageTk.PhotoImage(Image.open(iconname))
            self.mapView.set_marker(coords.lat, coords.lon, icon=marker, icon_anchor='s')
        else:
            self.mapView.set_marker(coords.lat, coords.lon)

    def removeMarkers(self):
        """Remove all markers."""
        self.mapView.delete_all_marker()

    def setDefaultLocation(self):
        """Display the default location on the map."""
        self.setLatLonZoom(self.locZero)

    def onRightClick(self, coords):
        self.mapView.set_position(coords[0], coords[1])
        
    def createWidgets(self, parent: tk.Frame, padx=0, pady=0):
        """Create user widgets."""
        self.mapView = tkintermapview.TkinterMapView(parent, width=600, height=400)
        self.mapView.pack(padx=padx, pady=pady)
        self.mapView.add_right_click_menu_command(label='Centrer ici',
            command=self.onRightClick, pass_coords=True)
        self.setDefaultLocation()
    
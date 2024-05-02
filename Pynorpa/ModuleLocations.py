"""
 Pynorpa Module for displaying and editing locations.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
from TabsApp import *
from TableLocations import *
from LocationCache import *
from LocationEditor import *
from MapWidget import *


class ModuleLocations(TabModule):
    """Pynorpa Module for locations."""
    log = logging.getLogger('ModuleLocations')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        self.table = TableLocations(self.onSelectLocation)
        self.mapWidget = MapWidget()
        self.editor = LocationEditor(self.onSaveLocation)
        super().__init__(parent, 'Lieux')
        self.locationCache = LocationCache()
        self.locationCache.load()
        self.table.loadData(self.locationCache.getLocations())

    def onSelectLocation(self, location: Location):
        self.log.info(f'Selected {location}')
        # Display in map widget
        self.mapWidget.loadData(location)
        # Display in editor
        self.editor.loadData(location)

    def onSaveLocation(self, location: Location):
        pass

    def createWidgets(self):
        """Create user widgets."""

        # Frames
        self.frmLeft = tk.Frame(master=self.oFrame)
        self.frmLeft.pack(fill=tk.Y, side=tk.LEFT, pady=0)
        self.frmRight = tk.Frame(master=self.oFrame)
        self.frmRight.pack(fill=tk.Y, side=tk.LEFT, pady=6, padx=6)

        # Locations table
        self.table.createWidgets(self.frmLeft)

        # Map widget
        self.mapWidget.createWidgets(self.frmRight)

        # Location editor
        self.editor.createWidgets(self.frmRight)
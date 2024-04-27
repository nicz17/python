"""
Table widget for Pynorpa Locations.
Subclass of BaseTable.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
from BaseTable import *
from LocationCache import *


class TableLocations(BaseTable):
    """Table widget for Pynorpa Locations."""
    log = logging.getLogger("TableLocations")

    def __init__(self, cbkSelect):
        """Constructor with selection callback."""
        self.log.info('Constructor')
        super().__init__(self.onRowSelection, 'locations')
        self.columns = ('Nom', 'Région', 'Altitude')
        self.data = []
        self.cbkSelect = cbkSelect

    def loadData(self, locations):
        """Display the specified locations in this table."""
        self.log.info('Loading %d locations', len(locations))
        self.clear()
        self.data = locations

        location: Location
        for location in locations:
            rowData = (location.name, location.lat, location.lon)
            self.addRow(rowData)

    def createWidgets(self, parent: tk.Frame):
        """Create user widgets."""
        super().createWidgets(parent, self.columns)

    def onRowSelection(self, event):
        """Row selection callback."""
        idxRow = self.getSelectedRow()
        self.cbkSelect(self.data[idxRow] if idxRow else None)
    

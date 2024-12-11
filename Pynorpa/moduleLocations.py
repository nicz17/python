"""
 Pynorpa Module for displaying and editing locations.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
from TabsApp import *
from BaseTable import *
from LocationCache import *
from MapWidget import *
import BaseWidgets


class ModuleLocations(TabModule):
    """Pynorpa Module for locations."""
    log = logging.getLogger('ModuleLocations')

    def __init__(self, parent: TabsApp) -> None:
        """Constructor."""
        self.window = parent.window
        self.table = TableLocations(self.onSelectLocation)
        self.mapWidget = MapWidget()
        self.editor = LocationEditor(self.onSaveLocation, self.mapWidget)
        super().__init__(parent, 'Lieux')

    def loadData(self):
        self.locationCache = LocationCache()
        self.table.loadData(self.locationCache.getLocations())

    def onSelectLocation(self, location: Location):
        self.log.info(f'Selected {location}')
        # Display in widgets
        self.mapWidget.loadData(location)
        self.editor.loadData(location)

    def onSaveLocation(self, location: Location):
        """Update the specified location in database."""
        self.log.info('Saving %s', location)
        self.locationCache.save(location)
        self.editor.loadData(location)

    def createWidgets(self):
        """Create user widgets."""
        self.createLeftRightFrames()

        # Location widgets
        self.table.createWidgets(self.frmLeft)
        self.mapWidget.createWidgets(self.frmRight)
        self.editor.createWidgets(self.frmRight)


class TableLocations(TableWithColumns):
    """Table widget for Pynorpa Locations."""
    log = logging.getLogger("TableLocations")

    def __init__(self, cbkSelect):
        """Constructor with selection callback."""
        self.log.info('Constructor')
        super().__init__(cbkSelect, 'locations')
        self.addColumn(TableColumn('Nom',      Location.getName,     200))
        self.addColumn(TableColumn('Région',   Location.getRegion,   150))
        self.addColumn(TableColumn('Altitude', Location.getAltitude,  80))

    def loadData(self, locations):
        """Display the specified locations in this table."""
        self.log.info('Loading %d locations', len(locations))
        self.clear()
        self.data = locations
        self.addRows(locations)

    def createWidgets(self, parent: tk.Frame):
        """Create user widgets."""
        super().createWidgets(parent)


class LatLonZoomWidget(BaseWidgets.BaseWidget):
    """A widget for displaying Lat/Lon/zoom info linked to a MapWidget."""
    log = logging.getLogger('LatLonZoomWidget')

    def __init__(self, cbkModified, mtdGetter, oMap: MapWidget):
        """Constructor with modification callback."""
        super().__init__(cbkModified, mtdGetter)
        self.value = LatLonZoom(0, 0, 10)
        self.oMap = oMap

    def setValue(self, object):
        """Set the boolean value."""
        self.value = self.getObjectValue(object)
        self.loadData()

    def getValue(self) -> LatLonZoom:
        """Get the current lat/lon/zoom value."""
        return self.value
    
    def loadData(self):
        if self.value is None:
            self.lblValue.configure(text='')
        else:
            self.lblValue.configure(text=self.value.toPrettyString())
    
    def onLinkMap(self):
        self.value = self.oMap.getLatLonZoom()
        self.loadData()
        self.cbkModified()
        
    def createWidgets(self, parent: tk.Frame, row: int, col: int):
        """Create widget in parent frame with grid layout."""
        self.oWidget = ttk.Frame(parent)
        self.lblValue = ttk.Label(self.oWidget, width=46, text='')
        self.lblValue.grid(row=0, column=0, sticky='we')
        self.btnMap = ttk.Button(self.oWidget, text='Lire la carte', command=self.onLinkMap)
        self.btnMap.grid(row=0, column=1, sticky='e')
        self.oWidget.grid(row=row, column=col, padx=5, sticky='we')

    def enableWidget(self, enabled: bool):
        BaseWidgets.enableWidget(self.btnMap, enabled)

class LocationEditor(BaseWidgets.BaseEditor):
    """A widget for editing Pynorpa locations."""
    log = logging.getLogger(__name__)

    def __init__(self, cbkSave, oMap: MapWidget):
        """Constructor with save callback."""
        super().__init__(cbkSave, '#62564f')
        self.location = None
        self.oMap = oMap

    def loadData(self, location: Location):
        """Display the specified object in this editor."""
        self.location = location
        self.setValue(location)

    def onSave(self, evt = None):
        """Save changes to the edited object."""
        self.location.setDesc(self.txtDesc.getValue())
        self.location.setLatLonZoom(self.widPosition.getValue())
        self.cbkSave(self.location)

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Location Editor')

        # Location attributes
        self.txtName     = self.addText('Nom', Location.getName)
        self.txtDesc     = self.addTextArea('Description', Location.getDesc, 6)
        self.txtState    = self.addText('Pays', Location.getState)
        self.txtRegion   = self.addText('Région', Location.getRegion)
        self.intAltitude = self.addIntInput('Altitude', Location.getAltitude, 'm')
        self.widPosition = self.addCustomWidget('Position', 
            LatLonZoomWidget(self.onModified, Location.getLatLonZoom, self.oMap))

        # Buttons: save, cancel
        self.createButtons(True, True, False)
        self.enableWidgets()

    def enableWidgets(self, evt=None):
        """Enable our internal widgets."""
        editing  = self.location is not None
        modified = self.hasChanges(self.location)
        super().enableWidgets(editing)
        self.enableButtons(modified, modified, False)
        self.txtDesc.resetModified()

    def __str__(self) -> str:
        return 'LocationEditor'
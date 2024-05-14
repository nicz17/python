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
        self.editor = LocationEditor(self.onSaveLocation)
        super().__init__(parent, 'Lieux')
        self.locationCache = LocationCache()
        self.locationCache.load()
        self.table.loadData(self.locationCache.getLocations())

    def onSelectLocation(self, location: Location):
        self.log.info(f'Selected {location}')
        # Display in widgets
        self.mapWidget.loadData(location)
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

        # Location widgets
        self.table.createWidgets(self.frmLeft)
        self.mapWidget.createWidgets(self.frmRight)
        self.editor.createWidgets(self.frmRight)


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
            rowData = (location.name, location.region, location.alt)
            self.addRow(rowData)

    def createWidgets(self, parent: tk.Frame):
        """Create user widgets."""
        super().createWidgets(parent, self.columns)

    def onRowSelection(self, event):
        """Row selection callback."""
        idxRow = self.getSelectedRow()
        self.cbkSelect(self.data[idxRow] if idxRow is not None else None)


class LocationEditor(BaseWidgets.BaseEditor):
    """A widget for editing Pynorpa locations."""
    log = logging.getLogger(__name__)

    def __init__(self, cbkSave):
        """Constructor with save callback."""
        super().__init__(cbkSave)
        self.location = None

    def loadData(self, location: Location):
        """Display the specified object in this editor."""
        self.location = location
        self.enableWidgets()
        self.txtName.setValue(None)
        self.txtState.setValue(None)
        self.txtRegion.setValue(None)
        self.txtDesc.setValue(None)
        self.intAltitude.setValue(None)
        self.lblPosition.setValue(None)
        if location:
            self.txtName.setValue(location.name)
            self.txtState.setValue(location.state)
            self.txtRegion.setValue(location.region)
            self.txtDesc.setValue(location.desc)
            self.intAltitude.setValue(location.alt)
            self.lblPosition.setValue(location.getGPSString())

    def hasChanges(self) -> bool:
        """Check if the editor has any changes."""
        if self.location:
            if self.location.name != self.txtName.getValue():
                return True
            if self.location.desc != self.txtDesc.getValue():
                return True
            if self.location.state != self.txtState.getValue():
                return True
            if self.location.region != self.txtRegion.getValue():
                return True
            if self.location.alt != self.intAltitude.getValue():
                return True
        return False

    def onSave(self, evt = None):
        """Save changes to the edited object."""
        #textEdit = self.txtInput.get(1.0, tk.END).strip()
        #self.task.title = textEdit
        self.cbkSave(self.location)

    def onCancel(self):
        """Cancel changes to the edited object."""
        self.loadData(self.location)

    def onDelete(self):
        """Delete the edited object."""
        pass

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Location Editor')

        # Location attributes
        self.txtName     = self.addText('Nom')
        self.txtDesc     = self.addTextArea('Description', 6)
        self.txtState    = self.addText('Pays')
        self.txtRegion   = self.addText('Région')
        self.intAltitude = self.addIntInput('Altitude')
        self.lblPosition = self.addTextReadOnly('Position')

        # Buttons: save, cancel
        frmButtons = ttk.Frame(self.frmEdit, padding=5)
        frmButtons.grid(row=self.row, column=0, columnspan=2)
        self.btnSave = tk.Button(frmButtons, text = 'Save', command = self.onSave)
        self.btnSave.grid(row=0, column=0, padx=3)
        self.btnCancel = tk.Button(frmButtons, text = 'Cancel', command = self.onCancel)
        self.btnCancel.grid(row=0, column=1, padx=3)
        self.btnDelete = tk.Button(frmButtons, text = 'Delete', command = self.onCancel)
        self.btnDelete.grid(row=0, column=2, padx=3)

        self.enableWidgets()

    def enableWidgets(self, evt=None):
        """Enable our internal widgets."""
        editing  = self.location is not None
        modified = self.hasChanges()
        self.txtName.enableWidget(editing)
        self.txtDesc.enableWidget(editing)
        self.txtState.enableWidget(editing)
        self.txtRegion.enableWidget(editing)
        self.intAltitude.enableWidget(editing)
        BaseWidgets.enableWidget(self.btnSave, modified)
        BaseWidgets.enableWidget(self.btnCancel, modified)
        BaseWidgets.enableWidget(self.btnDelete, False)
        self.txtDesc.resetModified()

    def __str__(self) -> str:
        return 'LocationEditor'
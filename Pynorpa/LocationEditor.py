"""
A widget for editing Pynorpa locations.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk
import BaseWidgets
import LocationCache


class LocationEditor():
    """A widget for editing LogBook tasks."""
    log = logging.getLogger(__name__)

    def __init__(self, cbkSave):
        """Constructor with save callback."""
        self.log.info('Constructor')
        self.cbkSave = cbkSave
        self.location = None
        self.row = 0

    def loadData(self, location: LocationCache.Location):
        """Display the specified object in this editor."""
        self.location = location
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
            self.lblPosition.setValue(f'lat {location.lat} lon {location.lon} zoom {location.zoom}')
        self.enableWidgets()

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

    def onModified(self, evt=None):
        """Callback for widget modifications."""
        #self.log.info('Location modified cbk')
        self.enableWidgets()

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        self.frmEdit = ttk.LabelFrame(parent, text='Location Editor')
        self.frmEdit.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, expand=True, pady=5)

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

    def addText(self, label: str) -> BaseWidgets.TextInput:
        """Add a single-line text input."""
        self.addLabel(label)
        oInput = BaseWidgets.TextInput(self.onModified)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.row += 1
        return oInput
    
    def addTextArea(self, label: str, nLines: int) -> BaseWidgets.TextArea:
        """Add a multi-line text input."""
        self.addLabel(label)
        oInput = BaseWidgets.TextArea(label, nLines, self.onModified)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.row += 1
        return oInput
    
    def addTextReadOnly(self, label: str) -> BaseWidgets.TextReadOnly:
        """Add a read-only text."""
        self.addLabel(label)
        oInput = BaseWidgets.TextReadOnly(label)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.row += 1
        return oInput
    
    def addIntInput(self, label: str) -> BaseWidgets.IntInput:
        """Add an integer input."""
        self.addLabel(label)
        oInput = BaseWidgets.IntInput(self.onModified)
        oInput.createWidgets(self.frmEdit, self.row, 1)
        self.row += 1
        return oInput

    def addLabel(self, label: str):
        """Add an attribute label at the specified row."""
        oLabel = tk.Label(self.frmEdit, text=label)
        oLabel.grid(row=self.row, column=0, sticky='nw')

    def enableWidgets(self, evt=None):
        """Enable our internal widgets."""
        modified = self.hasChanges()
        self.enableWidget(self.btnSave, modified)
        self.enableWidget(self.btnCancel, modified)
        self.enableWidget(self.btnDelete, False)
        #self.enableWidget(self.txtName, self.location is not None)
        #self.txtName.edit_modified(False)
        
    def enableWidget(self, widget: tk.Widget, enabled: bool):
        """Enable the specified tk widget if enabled is true."""
        if widget:
            widget['state'] = tk.NORMAL if enabled else tk.DISABLED

    def __str__(self) -> str:
        return 'LocationEditor'
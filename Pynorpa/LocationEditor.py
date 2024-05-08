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

    def loadData(self, location: LocationCache.Location):
        """Display the specified object in this editor."""
        self.location = location
        self.txtName.setValue(None)
        self.txtRegion.setValue(None)
        self.txtDesc.delete(1.0, tk.END)
        self.intAltitude.setValue(None)
        if location:
            self.txtName.setValue(location.name)
            self.txtRegion.setValue(location.region)
            self.txtDesc.insert(1.0, location.desc)
            self.intAltitude.setValue(location.alt)
        self.enableWidgets()

    def hasChanges(self) -> bool:
        """Check if the editor has any changes."""
        if self.location:
            if self.location.name != self.txtName.getValue():
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

        # Name
        self.txtName = self.addText(0, 'Nom')

        # Region
        self.txtRegion = self.addText(1, 'Région')

        # Description
        self.txtDesc = self.addTextArea(2, 'Description', 6)

        # Altitude
        self.intAltitude = self.addIntInput(3, 'Altitude')

        # Buttons: save, cancel
        frmButtons = ttk.Frame(self.frmEdit, padding=5)
        frmButtons.grid(row=4, column=0, columnspan=2)
        self.btnSave = tk.Button(frmButtons, text = 'Save', command = self.onSave)
        self.btnSave.grid(row=0, column=0, padx=3)
        self.btnCancel = tk.Button(frmButtons, text = 'Cancel', command = self.onCancel)
        self.btnCancel.grid(row=0, column=1, padx=3)
        self.btnDelete = tk.Button(frmButtons, text = 'Delete', command = self.onCancel)
        self.btnDelete.grid(row=0, column=2, padx=3)

    def addText(self, row: int, label: str) -> BaseWidgets.TextInput:
        """Add a single-line text input at the specified row."""
        self.addLabel(row, label)
        oInput = BaseWidgets.TextInput(self.onModified)
        oInput.createWidgets(self.frmEdit, row, 1)
        return oInput
    
    def addTextArea(self, iRow: int, sLabel: str, nLines: int) -> tk.Text:
        """Add a multi-line text input at the specified row."""
        self.addLabel(iRow, sLabel)
        oText = tk.Text(self.frmEdit, width=64, height=nLines)
        oText.grid(row=2, column=1, padx=4, sticky='we')
        return oText
    
    def addIntInput(self, row: int, label: str) -> BaseWidgets.IntInput:
        """Add an integer input at the specified row."""
        self.addLabel(row, label)
        oInput = BaseWidgets.IntInput(self.onModified)
        oInput.createWidgets(self.frmEdit, row, 1)
        return oInput

    def addLabel(self, iRow: int, sLabel: str):
        """Add an attribute label at the specified row."""
        oLabel = tk.Label(self.frmEdit, text=sLabel)
        oLabel.grid(row=iRow, column=0, sticky='nw')

    def enableWidgets(self, evt=None):
        """Enable our internal widgets."""
        modified = self.hasChanges()
        self.enableWidget(self.btnSave, modified)
        self.enableWidget(self.btnCancel, True)  # modified
        self.enableWidget(self.btnDelete, False)
        #self.enableWidget(self.txtName, self.location is not None)
        #self.txtName.edit_modified(False)
        
    def enableWidget(self, widget: tk.Widget, enabled: bool):
        """Enable the specified tk widget if enabled is true."""
        if widget:
            widget['state'] = tk.NORMAL if enabled else tk.DISABLED

    def __str__(self) -> str:
        return 'LocationEditor'
"""
A widget for editing Pynorpa locations.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk
from LocationCache import *


class LocationEditor():
    """A widget for editing LogBook tasks."""
    log = logging.getLogger(__name__)

    def __init__(self, cbkSave):
        """Constructor with save callback."""
        self.log.info('Constructor')
        self.cbkSave = cbkSave
        self.location = None

    def loadData(self, location: Location):
        """Display the specified object in this editor."""
        self.location = location
        self.txtName.delete(0, tk.END)
        self.txtRegion.delete(0, tk.END)
        self.txtDesc.delete(1.0, tk.END)
        if location:
            self.txtName.insert(0, location.name)
            self.txtRegion.insert(0, location.region)
            self.txtDesc.insert(1.0, location.desc)

    def onSave(self, evt = None):
        """Save changes to the edited object."""
        #textEdit = self.txtInput.get(1.0, tk.END).strip()
        #self.task.title = textEdit
        self.cbkSave(self.location)

    def onCancel(self):
        """Cancel changes to the edited object."""
        self.loadData(self.location)

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        self.frmEdit = ttk.LabelFrame(parent, text='Location Editor')
        self.frmEdit.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, expand=True, pady=5)

        # Name
        self.addLabel(0, 'Nom')
        self.txtName = self.addEntry(0)

        # Region
        self.addLabel(1, 'Région')
        self.txtRegion = self.addEntry(1)

        # Description
        self.addLabel(2, 'Description')
        self.txtDesc = tk.Text(self.frmEdit, width=64, height=6)
        self.txtDesc.grid(row=2, column=1, padx=4, sticky='ew')


        # Buttons: save, cancel
        frmButtons = ttk.Frame(self.frmEdit, padding=5)
        frmButtons.grid(row=3, column=0, columnspan=2)
        self.btnSave = tk.Button(frmButtons, text = 'Save', command = self.onSave)
        self.btnSave.grid(row=0, column=0)
        self.btnCancel = tk.Button(frmButtons, text = 'Cancel', command = self.onCancel)
        self.btnCancel.grid(row=0, column=1, padx=5)

    def addLabel(self, iRow: int, sLabel: str):
        """Add an attribute label at the specified row."""
        oLabel = tk.Label(self.frmEdit, text=sLabel)
        oLabel.grid(row=iRow, column=0, sticky='nw')

    def addEntry(self, iRow: int) -> ttk.Entry:
        """Add a ttk.Entry widget at the specified row."""
        oEntry = ttk.Entry(self.frmEdit, width=64)
        oEntry.grid(row=iRow, column=1, padx=5, sticky='ew')
        return oEntry

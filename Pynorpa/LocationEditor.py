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
        if location:
            self.txtName.insert(0, location.name)

    def onSave(self, evt = None):
        """Save changes to the edited object."""
        #textEdit = self.txtInput.get(1.0, tk.END).strip()
        #self.task.title = textEdit
        self.cbkSave(self.location)

    def onCancel(self):
        """Cancel changes to the edited object."""
        #self.loadData(self.location)

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        frmEdit = ttk.LabelFrame(parent, text='Location Editor')
        frmEdit.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, expand=True, pady=5)

        # Name
        self.lblName = tk.Label(frmEdit, text='Name')
        self.lblName.pack(anchor=tk.W)
        self.txtName = ttk.Entry(frmEdit)
        self.txtName.pack(anchor=tk.W, fill=tk.X)

        # Buttons frame
        frmButtons = ttk.Frame(frmEdit, padding=5)
        frmButtons.pack()
        
        # Save button
        self.btnSave = tk.Button(frmButtons, text = 'Save', command = self.onSave)
        self.btnSave.pack(side=tk.LEFT)
        
        # Cancel button
        self.btnCancel = tk.Button(frmButtons, text = 'Cancel', command = self.onCancel)
        self.btnCancel.pack(side=tk.LEFT, padx=5)

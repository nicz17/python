"""
A widget for editing LogBook steps.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk
from LogBookTask import *


class StepEditor():
    """A widget for editing LogBook steps."""
    log = logging.getLogger(__name__)

    def __init__(self, cbkSave):
        """Constructor with save callback."""
        self.log.info('Constructor')
        self.cbkSave = cbkSave
        self.step = None

    def loadData(self, step: LogBookStep):
        """Display the specified object in this editor."""
        self.step = step
        self.txtInput.delete(1.0, tk.END)
        self.lblStatus.configure(text = '')
        if step is not None:
            self.txtInput.insert(1.0, self.step.text)
            self.lblStatus.configure(text = f'Status: {step.status.name}')

    def onSave(self):
        """Save changes to the edited object."""
        textEdit = self.txtInput.get(1.0, tk.END).strip()
        self.step.text = textEdit
        self.cbkSave()

    def onCancel(self):
        """Cancel changes to the edited object."""
        self.loadData(self.step)

    def onDone(self):
        """Set step status as Done."""
        self.step.status = Status.Done
        self.onSave()

    def build(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        frmEdit = ttk.LabelFrame(parent, text='Step Editor')
        frmEdit.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, expand=True, pady=5)

        # Status label
        self.lblStatus = tk.Label(frmEdit, text='Status')
        self.lblStatus.pack(anchor=tk.W)

        # Step TextBox
        tk.Label(frmEdit, text='Text:').pack(anchor=tk.W)
        self.txtInput = tk.Text(frmEdit, height=5, width=42)
        self.txtInput.pack(fill=tk.X, expand=True, padx=3)
        self.txtInput.bind("<<Modified>>", self.enableWidgets)

        # Buttons frame
        frmButtons = ttk.Frame(frmEdit, padding=5)
        frmButtons.pack()
        
        # Save button
        self.btnSave = tk.Button(frmButtons, text = 'Save', command = self.onSave)
        self.btnSave.pack(side=tk.LEFT)
        
        # Cancel button
        self.btnCancel = tk.Button(frmButtons, text = 'Cancel', command = self.onCancel)
        self.btnCancel.pack(side=tk.LEFT, padx=5)
        
        # Done button
        self.btnDone = tk.Button(frmButtons, text = 'Done', command = self.onDone)
        self.btnDone.pack(side=tk.LEFT)

        self.enableWidgets()

    def hasChanges(self) -> bool:
        """Check if the editor has any changes."""
        if self.step is None:
            return False
        textEdit = self.txtInput.get(1.0, tk.END).strip()
        if self.step.text != textEdit:
            return True
        return False

    def enableWidgets(self, evt = None):
        """Enable our internal widgets."""
        modified = self.hasChanges()
        enableDone = self.step and self.step.status is not Status.Done
        self.enableButton(self.btnSave, modified)
        self.enableButton(self.btnCancel, modified)
        self.enableButton(self.btnDone, enableDone)
        self.txtInput.edit_modified(False)
        
    def enableButton(self, btn: tk.Button, bEnabled: bool):
        """Enable the specified button if bEnabled is true."""
        if btn:
            if bEnabled:
                btn['state'] = tk.NORMAL
            else:
                btn['state'] = tk.DISABLED
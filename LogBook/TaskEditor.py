"""
A widget for editing LogBook tasks.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
import DateTools
from tkinter import ttk
from LogBookTask import *


class TaskEditor():
    """A widget for editing LogBook tasks."""
    log = logging.getLogger(__name__)

    def __init__(self, cbkSave):
        """Constructor with save callback."""
        self.log.info('Constructor')
        self.cbkSave = cbkSave
        self.task = None

    def loadData(self, task: LogBookTask):
        """Display the specified object in this editor."""
        self.task = task
        self.enableWidgets()
        self.txtInput.delete(1.0, tk.END)
        self.lblStatus.configure(text = 'Status')
        self.lblCreated.configure(text = 'Created')
        if task is not None:
            sCreated = DateTools.timestampToString(task.created)
            self.txtInput.insert(1.0, self.task.title)
            self.lblCreated.configure(text = f'Created: {sCreated}')
            self.lblStatus.configure(text = f'Status: {task.status.name}')

    def onSave(self, evt = None):
        """Save changes to the edited object."""
        textEdit = self.txtInput.get(1.0, tk.END).strip()
        self.task.title = textEdit
        self.cbkSave()

    def onCancel(self):
        """Cancel changes to the edited object."""
        self.loadData(self.task)

    def onDone(self):
        """Set task status as Done."""
        self.task.status = Status.Done
        self.onSave()

    def build(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        frmEdit = ttk.LabelFrame(parent, text='Task Editor')
        frmEdit.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, expand=True, pady=5)

        # Creation time label
        self.lblCreated = tk.Label(frmEdit, text='Created')
        self.lblCreated.pack(anchor=tk.W)

        # Status label
        self.lblStatus = tk.Label(frmEdit, text='Status')
        self.lblStatus.pack(anchor=tk.W)

        # Task TextBox
        tk.Label(frmEdit, text='Title:').pack(anchor=tk.W)
        self.txtInput = tk.Text(frmEdit, height=2, width=42)
        self.txtInput.pack(fill=tk.X, expand=True, padx=3)
        self.txtInput.bind("<<Modified>>", self.enableWidgets)
        self.txtInput.bind("<Return>", self.onSave)

        # Buttons frame
        frmButtons = ttk.Frame(frmEdit, padding=5)
        frmButtons.pack()
        
        # Save button
        self.btnSave = tk.Button(frmButtons, text = 'Save', command = self.onSave)
        self.btnSave.pack(side=tk.LEFT)
        
        # Cancel button
        self.btnCancel = tk.Button(frmButtons, text = 'Cancel', command = self.onCancel)
        self.btnCancel.pack(side=tk.LEFT, padx=5)

        self.enableWidgets()

    def hasChanges(self) -> bool:
        """Check if the editor has any changes."""
        if self.task is None:
            return False
        textEdit = self.txtInput.get(1.0, tk.END).strip()
        if self.task.title != textEdit:
            return True
        return False

    def enableWidgets(self, evt = None):
        """Enable our internal widgets."""
        modified = self.hasChanges()
        self.enableWidget(self.btnSave, modified)
        self.enableWidget(self.btnCancel, modified)
        self.enableWidget(self.txtInput, self.task is not None)
        self.txtInput.edit_modified(False)
        
    def enableWidget(self, widget: tk.Widget, enabled: bool):
        """Enable the specified tk widget if enabled is true."""
        if widget:
            widget['state'] = tk.NORMAL if enabled else tk.DISABLED
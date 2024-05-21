"""
 Module for LogBook app widgets.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk
import BaseWidgets
from LogBookTask import *


class TaskEditor(BaseWidgets.BaseEditor):
    """A widget for editing LogBook tasks."""
    log = logging.getLogger('TaskEditor')

    def __init__(self, cbkSave):
        """Constructor with save callback."""
        super().__init__(cbkSave)
        self.task = None

    def loadData(self, task: LogBookTask):
        """Display the specified object in this editor."""
        self.task = task
        self.enableWidgets()
        self.txtTitle.setValue(None)
        self.lblStatus.setValue(None)
        self.lblCreated.setValue(None)
        if task is not None:
            sCreated = DateTools.timestampToString(task.created)
            self.txtTitle.setValue(task.title)
            self.lblCreated.setValue(sCreated)
            self.lblStatus.setValue(task.status.name)

    def hasChanges(self) -> bool:
        """Check if the editor has any changes."""
        if self.task is None:
            return False
        if self.task.title != self.txtTitle.getValue():
            return True
        return False

    def onSave(self, evt = None):
        """Save changes to the edited object."""
        self.task.title = self.txtTitle.getValue().strip()
        self.cbkSave()

    def onCancel(self):
        """Cancel changes to the edited object."""
        self.loadData(self.task)

    def onDone(self):
        """Set task status as Done."""
        self.task.status = Status.Done
        self.onSave()

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Task Editor')

        # Task attributes
        self.lblCreated = self.addTextReadOnly('Created')
        self.lblStatus  = self.addTextReadOnly('Status')
        self.txtTitle   = self.addTextArea('Title', 2, 42)
        self.txtTitle.oText.bind("<Return>", self.onSave)

        # Buttons: save, cancel
        frmButtons = ttk.Frame(self.frmEdit, padding=5)
        frmButtons.grid(row=self.row, column=0, columnspan=2)
        self.btnSave = tk.Button(frmButtons, text = 'Save', command = self.onSave)
        self.btnSave.grid(row=0, column=0, padx=3)
        self.btnCancel = tk.Button(frmButtons, text = 'Cancel', command = self.onCancel)
        self.btnCancel.grid(row=0, column=1, padx=3)

        self.enableWidgets()

    def enableWidgets(self, evt = None):
        """Enable our internal widgets."""
        modified = self.hasChanges()
        BaseWidgets.enableWidget(self.btnSave, modified)
        BaseWidgets.enableWidget(self.btnCancel, modified)
        self.txtTitle.enableWidget(self.task is not None)
        self.txtTitle.resetModified()


class StepEditor(BaseWidgets.BaseEditor):
    """A widget for editing LogBook steps."""
    log = logging.getLogger('TaskEditor')

    def __init__(self, cbkSave):
        """Constructor with save callback."""
        super().__init__(cbkSave)
        self.step = None

    def loadData(self, step: LogBookStep):
        """Display the specified object in this editor."""
        self.step = step
        self.enableWidgets()
        self.txtText.setValue(None)
        self.lblStatus.setValue(None)
        if step is not None:
            self.txtText.setValue(self.step.text)
            self.lblStatus.setValue(step.status.name)

    def onSave(self, evt = None):
        """Save changes to the edited object."""
        self.step.text = self.txtText.getValue().strip()
        self.cbkSave()

    def onCancel(self):
        """Cancel changes to the edited object."""
        self.loadData(self.step)

    def onDone(self):
        """Set step status as Done."""
        self.step.status = Status.Done
        self.onSave()

    def hasChanges(self) -> bool:
        """Check if the editor has any changes."""
        if self.step is None:
            return False
        if self.step.text != self.txtText.getValue():
            return True
        return False

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Step Editor')

        # Step attributes
        self.lblStatus = self.addTextReadOnly('Status')
        self.txtText   = self.addTextArea('Text', 6, 42)
        self.txtText.oText.bind("<Return>", self.onSave)

        # Buttons: save, cancel
        frmButtons = ttk.Frame(self.frmEdit, padding=5)
        frmButtons.grid(row=self.row, column=0, columnspan=2)
        self.btnSave = tk.Button(frmButtons, text = 'Save', command = self.onSave)
        self.btnSave.grid(row=0, column=0, padx=3)
        self.btnCancel = tk.Button(frmButtons, text = 'Cancel', command = self.onCancel)
        self.btnCancel.grid(row=0, column=1, padx=3)
        self.btnDone = tk.Button(frmButtons, text = 'Done', command = self.onDone)
        self.btnDone.grid(row=0, column=2, padx=3)

        self.enableWidgets()

    def enableWidgets(self, evt = None):
        """Enable our internal widgets."""
        modified = self.hasChanges()
        enableDone = self.step and self.step.status is not Status.Done
        BaseWidgets.enableWidget(self.btnSave, modified)
        BaseWidgets.enableWidget(self.btnCancel, modified)
        BaseWidgets.enableWidget(self.btnDone, enableDone)
        self.txtText.enableWidget(self.step is not None)
        self.txtText.resetModified()
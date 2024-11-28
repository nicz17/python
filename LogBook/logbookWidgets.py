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
#from BaseTable import *
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
        self.setValue(task)

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
        self.lblCreated = self.addTextReadOnly('Created', LogBookTask.getCreatedString)
        self.lblStatus  = self.addTextReadOnly('Status', LogBookTask.getStatusName)
        self.txtTitle   = self.addTextArea('Title', LogBookTask.getTitle, 2, 42)
        self.txtTitle.oWidget.bind("<Return>", self.onSave)

        # Buttons: save, cancel
        self.createButtons(True, True, False)
        self.enableWidgets()

    def enableWidgets(self, evt = None):
        """Enable our internal widgets."""
        modified = self.hasChanges(self.task)
        BaseWidgets.enableWidget(self.btnSave, modified)
        BaseWidgets.enableWidget(self.btnCancel, modified)
        self.txtTitle.enableWidget(self.task is not None)
        self.txtTitle.resetModified()


# class StepsTable(TableWithColumns):
#     """Table widget for Logbook steps."""
#     log = logging.getLogger("StepsTable")

#     def __init__(self, cbkSelect):
#         """Constructor with selection callback."""
#         self.log.info('Constructor')
#         super().__init__(cbkSelect, 'steps', 32)
#         self.addColumn(TableColumn('Status', LogBookStep.getStatusName,  60))
#         self.addColumn(TableColumn('Text',   LogBookStep.getText,       440))
#         #self.addColumn(TableColumn('Order',  LogBookStep.getOrder,       50))

#     def loadData(self, steps: list[LogBookStep]):
#         """Display the specified steps in this table."""
#         self.log.info('Loading %d steps', len(steps))
#         self.clear()
#         self.data = steps
#         self.addRows(steps)


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
        self.setValue(step)

    def onSave(self, evt=None):
        """Save changes to the edited object."""
        self.step.text  = self.txtText.getValue().strip()
        self.step.order = self.spiOrder.getValue()
        self.cbkSave()

    def onCancel(self):
        """Cancel changes to the edited object."""
        self.loadData(self.step)

    def onDone(self):
        """Set step status as Done."""
        self.step.status = Status.Done
        self.onSave()

    def createWidgets(self, parent: tk.Frame):
        """Add the editor widgets to the parent widget."""
        super().createWidgets(parent, 'Step Editor')

        # Step attributes
        self.lblStatus = self.addTextReadOnly('Status', LogBookStep.getStatusName)
        self.txtText   = self.addTextArea('Text', LogBookStep.getText, 6, 42)
        #self.intOrder  = self.addIntInput('Order', LogBookStep.getOrder)
        self.spiOrder  = self.addSpinBox('Order', LogBookStep.getOrder, 0, 999)
        self.txtText.oWidget.bind("<Return>", self.onSave)

        # Buttons: save, cancel, done
        self.createButtons(True, True, False)
        self.btnDone = self.addButton('Done', self.onDone)

        self.enableWidgets()

    def enableWidgets(self, evt = None):
        """Enable our internal widgets."""
        modified = self.hasChanges(self.step)
        editing  = self.step is not None
        enableDone = self.step and self.step.status is not Status.Done
        super().enableWidgets(editing)
        BaseWidgets.enableWidget(self.btnSave, modified)
        BaseWidgets.enableWidget(self.btnCancel, modified)
        BaseWidgets.enableWidget(self.btnDone, enableDone)
        self.txtText.resetModified()


class TaskProgress():
    """A progress bar for the selected task."""
    log = logging.getLogger(__name__)

    def __init__(self):
        """Constructor."""
        self.log.info('Constructor')
        self.progress = None
        self.label    = None

    def loadData(self, task: LogBookTask):
        """Update the progress bar."""
        fProgress = 0.0
        sLabel = 'No task selected'
        if task is not None:
            iTotal = task.countSteps()
            iDone  = task.countDoneSteps()
            sLabel = 'No steps in task'
            if iTotal > 0:
                fProgress = 100.0*iDone/iTotal
                sLabel = f'Done {iDone}/{iTotal} ({fProgress:.1f}%)'
        self.progress['value'] = fProgress
        self.label.configure(text=sLabel)

    def createWidgets(self, parent: tk.Frame):
        """Add the widgets to the parent frame."""
        frmProgress = ttk.LabelFrame(parent, text='Task Progress')
        frmProgress.pack(side=tk.TOP, anchor=tk.N, fill=tk.X, expand=True, pady=5)

        self.label = ttk.Label(frmProgress, text='No task selected')
        self.label.pack(fill=tk.X, expand=True, padx=5, pady=3)

        self.progress = ttk.Progressbar(frmProgress, orient='horizontal', mode='determinate')
        self.progress.pack(fill=tk.X, expand=True, padx=5, pady=3)
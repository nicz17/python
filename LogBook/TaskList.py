"""
A list displaying LogBook tasks.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.1"

import logging
import tkinter as tk
from LogBook import *
from LogBookTask import *


class TaskList():
    """A list displaying LogBook tasks."""
    log = logging.getLogger(__name__)

    def __init__(self, cbkSelect):
        """Constructor with selection callback."""
        self.log.info('Constructor')
        self.cbkSelect = cbkSelect
        self.book = None

    def loadData(self, book: LogBook):
        """Update rendering for the specified book."""
        self.book = book
        self.listTasks.delete(0, tk.END)
        if book is not None:
            idx = 1
            task: LogBookTask
            for task in self.book.tasks:
                self.listTasks.insert(idx, self.getTaskText(task))
                self.listTasks.itemconfig(tk.END, {'bg': task.status.getColor()})
                idx += 1

    def getTaskText(self, task: LogBookTask) -> str:
        """Get the text to display in this list for the specified task."""
        steps = task.countActiveSteps()
        count = '' if steps == 0 else f' ({steps})'
        return f'{task.title}{count}'

    def updateTask(self, task: LogBookTask):
        """Update the specified task in the list."""
        idx = self.getIndex(task)
        self.log.info(f'Updating {task} at row {idx}')
        self.listTasks.delete(idx)
        self.listTasks.insert(idx, self.getTaskText(task))
        self.listTasks.itemconfig(idx, {'bg': task.status.getColor()})
        
    def onSelection(self, evt):
        """ListBox selection event."""
        self.cbkSelect(self.getSelection())

    def getSelection(self) -> LogBookTask:
        """Get the selected task."""
        if len(self.listTasks.curselection()) == 0:
            return None
        index = int(self.listTasks.curselection()[0])
        return self.book.tasks[index]
    
    def setSelection(self, task: LogBookTask):
        """Set the listbox selection to the specified task."""
        for i in range(len(self.book.tasks)):
            if task == self.book.tasks[i]:
                self.listTasks.select_set(i)
                break
    
    def getIndex(self, task: LogBookTask):
        """Get the listbox index of the specified task."""
        for i in range(len(self.book.tasks)):
            if task == self.book.tasks[i]:
                return i

    def build(self, parent: tk.Frame):
        """Add the widgets to the parent frame."""
        self.listTasks = tk.Listbox(parent, 
            height = 20, width = 42,
            bg = "white", fg = "black")
        self.listTasks.bind('<<ListboxSelect>>', self.onSelection)
        self.listTasks.pack(fill=tk.Y, expand=True, pady=5)
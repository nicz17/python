"""
A list displaying LogBook tasks.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

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
                bgcolor = '#e0ffe0'
                nActive = task.countActiveSteps()
                text = task.title
                if nActive > 0:
                    text += f' ({nActive})'
                    bgcolor = '#ffffe0'
                self.listTasks.insert(idx, text)
                self.listTasks.itemconfig(tk.END, {'bg': bgcolor})
                idx += 1

    def getSelection(self) -> LogBookTask:
        """Get the selected task."""
        if len(self.listTasks.curselection()) == 0:
            return None
        index = int(self.listTasks.curselection()[0])
        return self.book.tasks[index]

    def build(self, parent: tk.Frame):
        """Add the widgets to the parent frame."""
        self.listTasks = tk.Listbox(parent, 
            height = 20, width = 36,
            bg = "white", fg = "black")
        self.listTasks.bind('<<ListboxSelect>>', self.cbkSelect)
        self.listTasks.pack(fill=tk.Y, expand=True, pady=5)
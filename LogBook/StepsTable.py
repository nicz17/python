"""
A table displaying LogBook steps.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk
from LogBookTask import *


class StepsTable():
    """A table displaying LogBook steps."""
    log = logging.getLogger(__name__)

    def __init__(self, cbkSelect):
        """Constructor with selection callback."""
        self.log.info('Constructor')
        self.cbkSelect = cbkSelect

    def build(self, parent: tk.Frame):
        """Add the widgets to the parent frame."""
        self.tree = ttk.Treeview(parent, height=32)
        self.tree['columns'] = ('status', 'text', 'order')

        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('status', anchor=tk.W, width=60)
        self.tree.column('text',   anchor=tk.W, width=440)
        self.tree.column('order',  anchor=tk.W, width=50)
        self.tree.heading('#0', text='', anchor=tk.W)
        self.tree.heading('status', text='Status', anchor=tk.W)
        self.tree.heading('text',   text='Text',   anchor=tk.W)
        self.tree.heading('order',  text='Order',  anchor=tk.W)
        self.tree.bind('<<TreeviewSelect>>', self.cbkSelect)
        self.tree.tag_configure('step-done', background=Status.Done.getColor())
        self.tree.tag_configure('step-todo', background=Status.Todo.getColor())
        self.tree.pack(pady=5)
    
    def loadData(self, task: LogBookTask):
        """Add steps from the specified task to the table."""
        self.tree.delete(*self.tree.get_children())

        if task is None:
            return
        
        idx = 0
        step: LogBookStep
        for step in task.steps:
            tag = 'step-todo'
            if step.status == Status.Done:
                tag = 'step-done'
            self.tree.insert(parent='', index='end', iid=idx, text='',
                values=(step.status.name, step.text, step.order), tags=(tag))
            idx += 1

    def getSelection(self) -> int:
        """Get the selected item in table."""
        sel = self.tree.focus()
        #self.log.info('Table selection: %s', sel)
        if len(sel) == 0:
            return None
        else:
            return int(sel)
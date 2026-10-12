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
        self.task = None
        self.ctxMenuActions = {}

    def build(self, parent: tk.Frame):
        """Add the widgets to the parent frame."""

        # Scrolling frame
        frmScroll = ttk.Frame(parent)
        frmScroll.pack(pady=5, anchor=tk.W)

        # Treeview
        self.tree = ttk.Treeview(frmScroll, height=32)
        self.tree['columns'] = ('status', 'text', 'order')
        
        # Scroll bar
        self.scrollbar = ttk.Scrollbar(frmScroll, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand = self.scrollbar.set)

        # Columns
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('status', anchor=tk.W, width=50)
        self.tree.column('text',   anchor=tk.W, width=450)
        self.tree.column('order',  anchor=tk.CENTER, width=50)
        self.tree.heading('#0', text='', anchor=tk.W)
        self.tree.heading('status', text='Status', anchor=tk.W)
        self.tree.heading('text',   text='Text',   anchor=tk.W)
        self.tree.heading('order',  text='Order',  anchor=tk.W)
        self.tree.bind('<<TreeviewSelect>>', self.cbkSelect)
        self.tree.bind("<Button-3>", self.onRightClick)
        self.tree.tag_configure('step-done', background=Status.Done.getColor())
        self.tree.tag_configure('step-todo', background=Status.Todo.getColor())

        # Pack
        self.tree.pack(side=tk.LEFT, pady=0)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # Contextual menu
        self.ctxMenuActions = {
            'reopen': 'Reopen step',
            'cancel': 'Cancel step',
            'delete': 'Delete step'
        }
        self.popup = tk.Menu(parent.winfo_toplevel(), tearoff=0)
        self.popup.add_command(label=self.ctxMenuActions['reopen'], command=self.onReopen)
        self.popup.add_command(label=self.ctxMenuActions['cancel'], state="disabled")
        self.popup.add_command(label=self.ctxMenuActions['delete'], state="disabled")
        self.popup.add_separator()
        self.popup.add_command(label='Close menu')
    
    def loadData(self, task: LogBookTask):
        """Add steps from the specified task to the table."""
        self.tree.delete(*self.tree.get_children())
        self.task = task
        if task is None:
            return
        
        idx = 0
        step: LogBookStep
        for step in task.steps:
            tag = 'step-todo'
            if step.status == Status.Done:
                tag = 'step-done'
            self.tree.insert(parent='', index='end', iid=idx, text='',
                values=(step.getStatusName(), step.getText(), step.getOrderStr()), tags=(tag))
            idx += 1

    def getSelection(self) -> int:
        """Get the selected item in table."""
        sel = self.tree.focus()
        #self.log.info('Table selection: %s', sel)
        if len(sel) == 0:
            return None
        else:
            return int(sel)
        
    def onRightClick(self, event):
        """Right-click event callback."""
        item = self.tree.identify_row(event.y)
        if item and self.task:
            idxRow = int(item)
            step = self.task.steps[idxRow]
            self.log.info(f'Right-click at {event.x}, {event.y}: {item} {step}')
            self.openContextMenu(idxRow, step, event.x_root, event.y_root)
        else:
            self.popup.unpost()

    def openContextMenu(self, idxRow: int, step: LogBookStep, x: int, y: int):
        if step:
            self.tree.focus(idxRow)
            self.tree.selection_set(idxRow)
            state = 'normal' if step.status == Status.Done else 'disabled'
            self.popup.entryconfig(self.ctxMenuActions['reopen'], state=state)
            self.popup.entryconfig(self.ctxMenuActions['delete'], state="disabled")
        try:
            self.popup.tk_popup(x, y)
        finally:
            self.popup.grab_release()

    def onReopen(self):
        pass
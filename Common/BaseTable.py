"""
Superclass for table widget, using a Ttk Tree.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk


class BaseTable():
    """A table widget."""
    log = logging.getLogger(__name__)

    def __init__(self, cbkSelect):
        """Constructor with selection callback."""
        self.log.info('Constructor')
        self.cbkSelect = cbkSelect
        
    def createWidgets(self, parent: tk.Frame, columns):
        """Create user widgets."""
        self.tree = ttk.Treeview(parent, height=32)
        self.tree['columns'] = columns

        # Define columns
        self.tree.column('#0', width=0, stretch=tk.NO)
        for sColName in columns:
            self.tree.column(sColName, anchor=tk.W)

        # Define headings
        self.tree.heading('#0', text='', anchor=tk.W)
        for sColName in columns:
            self.tree.heading(sColName, text=sColName, anchor=tk.W)

        self.tree.bind('<<TreeviewSelect>>', self.cbkSelect)
        self.tree.pack(pady=5)

    def getSelectedRow(self) -> int:
        """Get the selected row index."""
        sel = self.tree.focus()
        #self.log.info('Table selection: %s', sel)
        if len(sel) == 0:
            return None
        else:
            return int(sel)

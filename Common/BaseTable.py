"""
Superclass for table widget, using a Ttk Treeview.
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

    def __init__(self, cbkSelectRow, objectLabel = 'rows'):
        """Constructor with row selection callback."""
        self.log.info('Constructor')
        self.cbkSelectRow = cbkSelectRow
        self.objectlabel = objectLabel
        self.nRows = 0
        
    def createWidgets(self, parent: tk.Frame, columns):
        """Create user widgets."""
        self.tree = ttk.Treeview(parent, height=36)
        self.tree['columns'] = columns

        # Define columns
        self.tree.column('#0', width=0, stretch=tk.NO)
        for sColName in columns:
            self.tree.column(sColName, anchor=tk.W)

        # Define headings
        self.tree.heading('#0', text='', anchor=tk.W)
        for sColName in columns:
            self.tree.heading(sColName, text=sColName, anchor=tk.W)

        self.tree.bind('<<TreeviewSelect>>', self.cbkSelectRow)
        self.tree.pack(pady=5, anchor=tk.W)

        # Status and toolbar frame
        self.frmToolBar = tk.Frame(parent)
        self.frmToolBar.pack(fill=tk.X, anchor=tk.W)
        self.lblStatus = tk.Label(master=self.frmToolBar)
        self.lblStatus.pack(fill=tk.X, side=tk.LEFT) 

    def addRow(self, rowData):
        """Add a row to this table."""
        idx = self.nRows
        self.tree.insert(parent='', index='end', iid=idx, text='', values=rowData)
        self.nRows += 1
        self.lblStatus.configure(text=f'{self.nRows} {self.objectlabel}')

    def getSelectedRow(self) -> int:
        """Get the selected row index."""
        sel = self.tree.focus()
        #self.log.info('Table selection: %s', sel)
        if len(sel) == 0:
            return None
        else:
            return int(sel)
        
    def clear(self):
        """Clears the tree contents."""
        self.tree.delete(*self.tree.get_children())
        self.nRows = 0
        self.lblStatus.configure(text=f'No {self.objectlabel}')

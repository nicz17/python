"""
Superclass for tree widget, using a Ttk Treeview.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk


class BaseTree():
    """A tree widget."""
    log = logging.getLogger(__name__)

    def __init__(self, cbkSelectItem):
        """Constructor with item selection callback."""
        self.log.info('Constructor')
        self.cbkSelectItem = cbkSelectItem

    def createWidgets(self, parent: tk.Frame):
        """Create user widgets."""
        self.tree = ttk.Treeview(parent, height=36)
        self.tree.bind('<<TreeviewSelect>>', self.cbkSelectItem)
        self.tree.pack(pady=5, anchor=tk.W)

    def addItem(self, id: str, text: str, parentId: str):
        """Add an item to the tree, possibly as a child."""
        if parentId is None:
            parentId = ""
        elif not self.tree.exists(parentId):
            self.log.error('Could not find parent item %s, aborting', parentId)
            return None
        iid = self.tree.insert(parentId, tk.END, text=text, iid=id)
        self.log.info('Added item %s %s', iid, text)
        return iid

    def addTestItems(self):
        """Add test data to the tree."""
        self.log.info('Adding test items to tree')
        id = self.addItem('EU', 'Europe', None)
        self.addItem('FR', 'France', id)
        self.addItem('IT', 'Italie', id)
        id = self.addItem('AFR', 'Africa', None)
        self.addItem('BF', 'Burkina Faso', id)
        self.addItem('PN', 'Pole Nord', 'nrdpl')

    def getSelectedId(self) -> str:
        """Get first selected item id, or None if no selection."""
        sel = self.tree.selection()
        if len(sel) > 0:
            return sel[0]
        return None

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

"""
Superclass for tree widget, using a Ttk Treeview.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk
from Timer import Timer
from BaseWidgets import ContextMenu


class BaseTree():
    """A tree widget."""
    log = logging.getLogger(__name__)

    def __init__(self, title: str, cbkSelection, cbkRightClick=None):
        """Constructor with item selection callback."""
        self.log.info(f'Constructor for {title}')
        self.title = title
        self.cbkSelection = cbkSelection
        self.cbkRightClick = cbkRightClick
        self.nItems = 0
        self.ctxtmenu = None

    def onRightClick(self, event=None):
        iid = self.tree.identify_row(event.y)
        self.log.info(f'Right-click {event} {iid}')
        if self.cbkRightClick:
            self.tree.focus(iid)
            self.tree.selection_set(iid)
            self.cbkRightClick(event, iid)
        #self.selectRow(row)
        #if self.ctxtmenu and event:
        #    self.ctxtmenu.show(event.x_root, event.y_root, self.selobj)

    def createWidgets(self, parent: tk.Frame):
        """Create user widgets."""

        # Styles
        style = ttk.Style()
        style.configure('Count.TLabel', foreground='grey')
        style.configure("Bold.TLabel",  font=("Helvetica", 11, "bold"))

        # Frames
        self.frmMain = ttk.Frame(parent)
        self.frmMain.pack(pady=5, anchor=tk.W)
        self.frmHead = ttk.Frame(self.frmMain)
        self.frmHead.grid(column=0, row=0, sticky='we')

        # Title bar
        self.lblTitle = ttk.Label(self.frmHead, text=self.title, justify="left", style="Bold.TLabel")
        self.lblTitle.pack(side='left')
        self.lblCount = ttk.Label(self.frmHead, justify="right", style='Count.TLabel')
        self.lblCount.pack(side='right')

        # Tree
        self.tree = ttk.Treeview(self.frmMain, show='tree', height=36)
        self.tree.column('#0', width=535)
        self.tree.bind('<<TreeviewSelect>>', self.cbkSelection)
        self.tree.bind('<Button-3>', self.onRightClick)
        #self.tree.pack(pady=5, anchor=tk.W)
        self.tree.grid(column=0, row=1, sticky='we')

    def addItem(self, id: str, text: str, parentId: str, tag=None, icon=None):
        """Add an item to the tree, possibly as a child."""
        if parentId is None:
            parentId = ""
        elif not self.tree.exists(parentId):
            self.log.error('Could not find parent item %s, aborting', parentId)
            return None
        tags = []
        if tag:
            tags.append(tag)
        if icon:
            iid = self.tree.insert(parentId, tk.END, text=text, iid=id, image=icon)
        else:
            iid = self.tree.insert(parentId, tk.END, text=text, iid=id, tags=tags)
        #self.log.info('Added item %s %s', iid, text)
        self.nItems += 1
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
        if len(sel) == 0:
            return None
        else:
            return int(sel)

    def setSelection(self, obj):
        """Set the tree selection to the specified object."""
        if obj:
            iid = str(obj.getIdx())
            self.tree.see(iid)
            self.tree.focus(iid)
            self.tree.selection_set(iid)

    def setStatus(self, timer: Timer):
        """Set the status label with tem count and load time."""
        status = f'{self.size()} | {timer.getElapsed()}'
        self.lblCount.config(text=status)
        
    def size(self):
        """Returns the number of items in the tree."""
        return self.nItems
        
    def clear(self):
        """Clears the tree contents."""
        self.tree.delete(*self.tree.get_children())
        self.nItems = 0

    def addContextMenuAction(self, label: str, cmdExecute, cbkEnable):
        if self.ctxtmenu is None:
            self.ctxtmenu = ContextMenu(self.frmMain.winfo_toplevel(), f'BaseTree {self.title}')
        self.ctxtmenu.addAction(label, cmdExecute, cbkEnable)

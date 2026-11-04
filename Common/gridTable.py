"""
A table using a tkinter grid layout.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk
from pathlib import Path

from BaseWidgets import IconButton, SearchBar
from Timer import Timer


class TableColumn():
    """A table column."""
    log = logging.getLogger('TableColumn')

    def __init__(self, label: str, mtdGetter, width=100):
        """Constructor with label, getter method, and width in pixels."""
        self.label = label
        self.mtdGetter = mtdGetter
        self.width = width

class GridTable:
    """A grid table."""
    log = logging.getLogger('GridTable')
    dirIcons = f'{Path.home()}/prog/icons'

    def __init__(self, title: str, cbkSelection):
        self.log.info(f'Constructor for GridTable {title}')
        self.iconOk = tk.PhotoImage(file=f'{self.dirIcons}/ok18.png')
        self.cbkSelection = cbkSelection
        self.title = title
        self.columns = []
        self.data = []
        self.widgets = {}

    def onSearch(self, search: str):
        """Search bar callback. Look for a matching record and select it."""
        for row, obj in enumerate(self.data):
            for col in self.getColumns():
                value = col.mtdGetter(obj)
                if isinstance(value, str) and search.lower() in value.lower():
                    self.log.info(f'{obj} matches {search}')
                    self.selectRow(row)
                    return
        self.log.info(f'No match for {search}')

    def onCellSelected(self, obj, row: int, event=None):
        self.log.info(f'Selected {obj} on row {row}')
        self.selectRow(row)

    def selectRow(self, row: int):
        """Select the given row. The first object is on row 0."""
        self.setSelectionStyle(row)
        if self.cbkSelection:
            self.cbkSelection(self.data[row] if row is not None else None)

    def selectObject(self, obj):
        """Select the given object by its getIdx()."""
        if obj is None:
            self.selectRow(None)
            return
        for row, o in enumerate(self.data):
            if obj.getIdx() == o.getIdx():
                self.selectRow(row)
                break

    def updateObject(self, obj):
        """Update the given object in table."""
        if obj is None:
            return
        for row, o in enumerate(self.data):
            if obj.getIdx() == o.getIdx():
                for icol, column in enumerate(self.columns):
                    value = column.mtdGetter(obj)
                    self.setCellValue(self.widgets[row][icol], value)

    def setSelectionStyle(self, row: int):
        for irow in range(len(self.data)):
            style = 'Sel.TLabel' if row == irow else 'Main.TLabel'
            for col in range(len(self.columns)):
                self.widgets[irow][col].config(style=style)   

    def addColumn(self, name: str, mtdGetter):
        self.columns.append(TableColumn(name, mtdGetter))

    def getColumns(self) -> list[TableColumn]:
        """Returns the table column definitions."""
        return self.columns

    def addRefreshButton(self, cbkRefresh):
        """Add an icon button to refresh table contents."""
        self.btnRefresh = IconButton(self.frmFoot, 'refresh', 'Recharger la table', cbkRefresh, 6)

    def addSearchBar(self):
        """Add a search bar."""
        self.searchBar = SearchBar(self.frmFoot, None, self.onSearch)

    def loadData(self, data: list):
        timer = Timer()
        self.data = data

        for irow, obj in enumerate(data):
            for icol, column in enumerate(self.columns):
                value = column.mtdGetter(obj)
                lblCell = ttk.Label(self.frmBody, justify="left", style='Main.TLabel')
                lblCell.grid(column=icol, row=irow+1, sticky='we', padx=4, pady=1)
                lblCell.bind("<Button-1>", lambda event, obj=obj, row=irow: self.onCellSelected(obj, row, event))
                self.setCellValue(lblCell, value)
                if not irow in self.widgets:
                    self.widgets[irow] = {}
                self.widgets[irow][icol] = lblCell

        count = len(data)
        perf = timer.getElapsed()
        self.lblCount.config(text=f'{count} | {perf}')

    def setCellValue(self, lblCell: ttk.Label, value):
        if isinstance(value, str):
            lblCell.config(text=value)
        elif isinstance(value, bool):
            icon = self.iconOk if value else None
            lblCell.config(image=icon)

    def createWidgets(self, parent: ttk.Frame):
        """Create user widgets."""

        # Styles
        style = ttk.Style()
        style.configure('Main.TFrame',  background='#f1f1f1')
        style.configure('Main.TLabel',  background='#f1f1f1')
        style.configure('Sel.TLabel',   background='#e0e0ff')
        style.configure('Count.TLabel', foreground='grey')
        style.configure("Bold.TLabel", font=("Helvetica", 11, "bold"))

        # Frames
        self.frmMain = ttk.Frame(parent)
        self.frmMain.pack(pady=6)
        self.frmMain.grid_columnconfigure(0, weight=1)
        self.frmHead = ttk.Frame(self.frmMain)
        self.frmHead.grid(column=0, row=0, sticky='we')
        self.frmBody = ttk.Frame(self.frmMain, relief=tk.SUNKEN, style='Main.TFrame')
        self.frmBody.grid(column=0, row=1)
        self.frmFoot = ttk.Frame(self.frmMain)
        self.frmFoot.grid(column=0, row=2, sticky='we')

        # Title bar
        self.lblTitle = ttk.Label(self.frmHead, text=self.title, justify="left", style="Bold.TLabel")
        self.lblTitle.pack(side='left')
        self.lblCount = ttk.Label(self.frmHead, justify="right", style='Count.TLabel')
        self.lblCount.pack(side='right')

        # Header cells
        for icol, column in enumerate(self.columns):
            frmHeader = ttk.Frame(self.frmBody)
            frmHeader.grid(column=icol, row=0, padx=1, pady=1, sticky='we')
            lblHeader = ttk.Label(frmHeader, text=column.label)
            lblHeader.pack(padx=3)

    def __str__(self):
        return f'GridTable {self.title}'
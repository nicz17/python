"""
A table using a tkinter grid layout.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.0"

import logging
import os
import tkinter as tk
from tkinter import ttk
from pathlib import Path

from BaseWidgets import IconButton, SearchBar
from Timer import Timer


class TableColumn():
    """A table column."""
    log = logging.getLogger('TableColumn')

    def __init__(self, label: str, mtdGetter, width=None):
        """Constructor with label, getter method, and width in pixels."""
        self.label = label
        self.mtdGetter = mtdGetter
        self.width = width

class GridTable:
    """A grid table."""
    log = logging.getLogger('GridTable')
    dirIcons = f'{Path.home()}/prog/icons'
    colorBg  = '#fdfdfd'
    colorSel = '#d0d0ff'

    def __init__(self, title: str, cbkSelection=None, height=500):
        self.log.info(f'Constructor for GridTable {title} height {height}px')
        self.cbkSelection = cbkSelection
        self.height = height
        self.nRows = None
        self.title = title
        self.columns = []
        self.data = []
        self.widgets = {}
        self.iconOk = None

    def loadIcons(self):
        """Load icons for boolean values."""
        filename = f'{self.dirIcons}/ok18.png'
        if os.path.exists(filename):
            self.iconOk = tk.PhotoImage(file=filename)
        else:
            self.log.warning(f'Could not find icon {filename}')

    def onSearch(self, search: str):
        """Search bar callback. Look for a matching record and select it."""
        for row, obj in enumerate(self.data):
            for col in self.getColumns():
                value = col.mtdGetter(obj)
                if isinstance(value, str) and search.lower() in value.lower():
                    self.log.info(f'{obj} matches {search}')
                    self.moveTo(row)
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

    def moveTo(self, row: int):
        if row is not None:
            position = row/self.nRows
            self.canvas.yview_moveto(position)

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

    def addColumn(self, name: str, mtdGetter, minWidth=None):
        """Add a table column for the given label and data accessor."""
        self.columns.append(TableColumn(name, mtdGetter, minWidth))

    def getColumns(self) -> list[TableColumn]:
        """Returns the table column definitions."""
        return self.columns

    def addRefreshButton(self, cbkRefresh):
        """Add an icon button to refresh table contents."""
        self.btnRefresh = IconButton(self.frmFoot, 'refresh', 'Recharger la table', cbkRefresh, 6)

    def addSearchBar(self):
        """Add a search bar."""
        self.searchBar = SearchBar(self.frmFoot, None, self.onSearch)

    def loadData(self, data: list, timer=None):
        if timer is None:
            timer = Timer()
        self.data = data
        self.log.info(f'Loading {len(data)} data rows')

        # Clear all cells
        for widget in self.frmBody.winfo_children():
            widget.destroy()

        # Header cells
        for icol, column in enumerate(self.columns):
            frmHeader = ttk.Frame(self.frmBody)
            frmHeader.grid(column=icol, row=0, padx=1, pady=2, sticky='we')
            lblHeader = ttk.Label(frmHeader, text=column.label)
            lblHeader.pack(padx=3, fill=tk.X)
            if column.width:
                self.frmBody.grid_columnconfigure(icol, minsize=column.width)

        # Fill each table cell
        for irow, obj in enumerate(data):
            for icol, column in enumerate(self.columns):
                value = column.mtdGetter(obj)
                lblCell = ttk.Label(self.frmBody, justify="left", style='Main.TLabel')
                lblCell.grid(column=icol, row=irow+1, sticky='we', padx=2, pady=1)
                lblCell.bind("<Button-1>", lambda event, obj=obj, row=irow: self.onCellSelected(obj, row, event))
                self.setCellValue(lblCell, value)
                if not irow in self.widgets:
                    self.widgets[irow] = {}
                self.widgets[irow][icol] = lblCell

        # Adjust table width
        self.adjustTableSize()

        # Display row count and timing in title bar
        heightFrame  = self.frmBody.winfo_height()
        heightCanvas = self.canvas.winfo_height()
        self.nRows = len(self.data)*heightCanvas//heightFrame
        self.log.info(f'Table height: {heightCanvas}/{heightFrame}px: {self.nRows} rows visible')
        nRowsDisplayed = min(self.nRows, len(data))
        count = f'{nRowsDisplayed}/{len(data)}'
        perf = timer.getElapsed()
        self.lblCount.config(text=f'{count} | {perf}')

    def adjustTableSize(self):
        # Update root window to have correct sizes
        root = self.frmMain.winfo_toplevel()
        root.update()

        # Adjust convas size if needed
        width  = self.frmBody.winfo_width()
        height = self.frmBody.winfo_height()
        self.log.info(f'Adjusting table size to {width}x{height}px')
        if width > 1:
            self.canvas.config(width=width)
        if height > 1:
            self.canvas.config(height=min(height, self.height))

        # Update root window to have correct sizes
        root.update()

    def setCellValue(self, lblCell: ttk.Label, value):
        if isinstance(value, str):
            lblCell.config(text=value)
        elif isinstance(value, bool):
            if self.iconOk:
                icon = self.iconOk if value else None
                lblCell.config(image=icon, anchor='center')
            else:
                svalue = 'Oui' if value else ''
                lblCell.config(text=svalue)
        elif isinstance(value, int):
            lblCell.config(text=str(value), anchor='e')
        else:
            self.log.error(f'Unhandled datatype for {value}')
            lblCell.config(text='Erreur!')

    def createWidgets(self, parent: ttk.Frame):
        """Create user widgets."""

        # Styles
        style = ttk.Style()
        style.configure('Main.TFrame',  background=self.colorBg)
        style.configure('Main.TLabel',  background=self.colorBg)
        style.configure('Sel.TLabel',   background=self.colorSel)
        style.configure('Count.TLabel', foreground='grey')
        style.configure("Bold.TLabel", font=("Helvetica", 11, "bold"))

        # Frames
        self.frmMain = ttk.Frame(parent)
        self.frmMain.pack(pady=6)
        #self.frmMain.grid_columnconfigure(0, weight=1)
        self.frmHead = ttk.Frame(self.frmMain)
        self.frmHead.grid(column=0, row=0, sticky='we', columnspan=2)

        self.canvas = tk.Canvas(self.frmMain, bd=0, highlightthickness=0, height=self.height)
        self.canvas.grid(column=0, row=1, sticky='nswe')

        scrollbar = ttk.Scrollbar(self.frmMain, orient=tk.VERTICAL)
        scrollbar.grid(column=1, row=1, sticky='nswe')
        scrollbar.config(command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        #self.frmBody = ttk.Frame(self.frmMain, relief=tk.SUNKEN, style='Main.TFrame')
        #self.frmBody.grid(column=0, row=1)
        self.frmBody = ttk.Frame(self.canvas, relief=tk.SUNKEN, style='Main.TFrame')
        self.canvas.create_window((0, 0), window=self.frmBody, anchor="nw")
        self.frmBody.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        #self.frmBody.bind_all("<Button-4>", self.onMouseWheel)
        #self.frmBody.bind_all("<Button-5>", self.onMouseWheel)
        self.frmBody.bind('<Enter>', self.bindMouseWheel)
        self.frmBody.bind('<Leave>', self.unbindMouseWheel)

        self.frmFoot = ttk.Frame(self.frmMain)
        self.frmFoot.grid(column=0, row=2, sticky='we', columnspan=2)

        # Title bar
        self.lblTitle = ttk.Label(self.frmHead, text=self.title, justify="left", style="Bold.TLabel")
        self.lblTitle.pack(side='left')
        self.lblCount = ttk.Label(self.frmHead, justify="right", style='Count.TLabel')
        self.lblCount.pack(side='right')

        self.loadIcons()

    def bindMouseWheel(self, event):
        self.frmBody.bind_all("<Button-4>", self.onMouseWheel)
        self.frmBody.bind_all("<Button-5>", self.onMouseWheel)

    def unbindMouseWheel(self, event):
        self.frmBody.unbind_all("<Button-4>")
        self.frmBody.unbind_all("<Button-5>")

    def onMouseWheel(self, event):
        # event.num is 4 for up, 5 for down
        amount = 2 if event.num == 5 else -2
        self.canvas.yview_scroll(amount, "units")

    def __str__(self):
        return f'GridTable {self.title}'
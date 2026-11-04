"""
A table using a tkinter grid layout.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk
from tkinter import ttk
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

    def __init__(self, title: str, cbkSelection):
        self.log.info(f'Constructor for GridTable {title}')
        self.cbkSelection = cbkSelection
        self.title = title
        self.columns = []
        self.data = []
        self.widgets = {}

    def onCellSelected(self, obj, row: int, event=None):
        self.log.info(f'Selected {obj} on row {row}')
        self.setSelectionStyle(row)
        if self.cbkSelection:
            self.cbkSelection(obj)

    def setSelectionStyle(self, row: int):
        for irow in range(len(self.data)):
            style = 'Sel.TLabel' if row == irow else 'Main.TLabel'
            for col in range(len(self.columns)):
                self.widgets[irow][col].config(style=style)   

    def addColumn(self, name: str, mtdGetter):
        self.columns.append(TableColumn(name, mtdGetter))

    def loadData(self, data: list):
        timer = Timer()
        self.data = data

        for irow, obj in enumerate(data):
            for icol, column in enumerate(self.columns):
                value = column.mtdGetter(obj)
                lblCell = ttk.Label(self.frmBody, text=value, justify="left", style='Main.TLabel')
                lblCell.grid(column=icol, row=irow+1, sticky='we', padx=4, pady=1)
                lblCell.bind("<Button-1>", lambda event, obj=obj, row=irow: self.onCellSelected(obj, row, event))
                if not irow in self.widgets:
                    self.widgets[irow] = {}
                self.widgets[irow][icol] = lblCell

        count = len(data)
        perf = timer.getElapsed()
        self.lblCount.config(text=f'{count}, {perf}')

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
        self.frmHead = ttk.Frame(self.frmMain)
        self.frmHead.grid(column=0, row=0, sticky='we')
        self.frmBody = ttk.Frame(self.frmMain, relief=tk.SUNKEN, style='Main.TFrame')
        self.frmBody.grid(column=0, row=1)
        self.frmFoot = ttk.Frame(self.frmMain)
        self.frmFoot.grid(column=0, row=2)

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
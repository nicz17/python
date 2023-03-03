"""
 Rendering methods for Qombo.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
from tkinter import font as tkfont
import logging
from BaseApp import *
from Grid import *
from Qombit import *
from Palette import *

class Renderer:
    gridW = 8
    gridH = 6
    iSize = 100
    iRadiusGrid = 36
    iRadiusSel  = 64

    """Rendering methods for Qombo."""
    log = logging.getLogger('Renderer')

    def __init__(self, grid: Grid, canGrid: tk.Canvas, canSelection: tk.Canvas):
        self.grid = grid
        self.canGrid = canGrid
        self.canSelection = canSelection
        self.fontBold = tkfont.Font(family="Helvetica", size=12, weight='bold')
        self.iHeight = self.gridH*self.iSize
        self.iWidth  = self.gridW*self.iSize

    def drawGrid(self):
        """Draw grid lines and qombits on the grid canvas"""
        self.canGrid.delete('all')
        self.drawGridLines()
        for x in range(self.gridW):
            for y in range(self.gridH):
                qombit = self.grid.get(x, y)
                self.drawQombit(x, y, qombit)

    def drawQombit(self, x, y, qombit: Qombit):
        """Draw the Qombit on the grid canvas."""
        if qombit:
            r = 36
            tx = x*self.iSize + 50
            ty = y*self.iSize + 50
            self.drawCircle(self.canGrid, tx, ty, self.iRadiusGrid, '#a0d0d0', qombit.getColor())
            self.canGrid.create_text(tx, ty, text = qombit.oKind)

    def drawGridLines(self):
        """Draw lines on the grid canvas"""
        for x in range(self.gridW):
            gx = x*self.iSize
            gy = self.iHeight
            self.canGrid.create_line(gx, 0, gx, gy, fill="#b0e0e0", width=1)
        for y in range(self.gridH):
            gx = self.iWidth
            gy = y*self.iSize
            self.canGrid.create_line(0, gy, gx, gy, fill="#b0e0e0", width=1)

    def drawSelection(self, qombit: Qombit):
        """Update the selection canvas"""
        self.canSelection.delete('all')
        if qombit:
            tx, ty = 100, 120
            self.canSelection.create_text(tx, 20, text = qombit.sName, font = self.fontBold)
            self.drawCircle(self.canSelection, tx, ty, self.iRadiusSel, '#d0d0a0', qombit.getColor())
            self.canSelection.create_text(tx, 220, text = str(qombit.oRarity) + ' ' + str(qombit.oKind))
            self.canSelection.create_text(tx, 240, text = 'Level ' + str(qombit.iLevel))
        else:
            self.canSelection.create_text(100, 20, text = 'Ready')

    def drawCircle(self, canvas: tk.Canvas, x:int, y: int, r: int, outline: str, fill: str):
        canvas.create_oval(x-r, y-r, x+r, y+r, outline=outline, fill=fill)

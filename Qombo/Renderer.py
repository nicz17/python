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
    iRadiusGrid = 36
    iRadiusSel  = 64

    """Rendering methods for Qombo."""
    log = logging.getLogger('Renderer')

    def __init__(self, grid: Grid, canGrid: tk.Canvas, canSelection: tk.Canvas, iSize: int):
        self.iSize = iSize
        self.grid = grid
        self.canGrid = canGrid
        self.canSelection = canSelection
        self.fontBold = tkfont.Font(family="Helvetica", size=12, weight='bold')
        self.iHeight = self.grid.h*self.iSize
        self.iWidth  = self.grid.w*self.iSize
        
        # Add image dir if missing
        if not os.path.exists(Qombit.sImageDir):
            os.makedirs(Qombit.sImageDir)

    def drawGrid(self):
        """Draw grid lines and qombits on the grid canvas"""
        self.canGrid.delete('all')
        self.drawGridLines()
        for x in range(self.grid.w):
            for y in range(self.grid.h):
                qombit = self.grid.get(x, y)
                self.drawQombit(x, y, qombit)

    def drawQombit(self, x, y, qombit: Qombit):
        """Draw the Qombit on the grid canvas."""
        if qombit:
            tx = x*self.iSize + 5
            ty = y*self.iSize + 5
            self.canGrid.create_image(tx, ty, anchor = tk.NW, image = qombit.getImage())

    def drawGridLines(self):
        """Draw lines on the grid canvas"""
        for x in range(self.grid.w):
            gx = x*self.iSize
            gy = self.iHeight
            self.canGrid.create_line(gx, 0, gx, gy, fill="#b0e0e0", width=1)
        for y in range(self.grid.h):
            gx = self.iWidth
            gy = y*self.iSize
            self.canGrid.create_line(0, gy, gx, gy, fill="#b0e0e0", width=1)

    def drawSelection(self, qombit: Qombit):
        """Update the selection canvas"""
        self.canSelection.delete('all')
        if qombit:
            tx, ty = 100, 120
            self.canSelection.create_text(tx, 20, text = qombit.sName, font = self.fontBold)
            self.canSelection.create_image(tx-80, ty-80, anchor = tk.NW, image = qombit.getImageLarge())
            self.canSelection.create_text(tx, 220, text = str(qombit.oRarity) + ' ' + str(qombit.oKind))
            self.canSelection.create_text(tx, 240, text = 'Level ' + str(qombit.iLevel))
            self.canSelection.create_text(tx, 300, text = qombit.getDescription())
        else:
            self.canSelection.create_text(100, 20, text = 'Ready')

    def drawCircle(self, canvas: tk.Canvas, x:int, y: int, r: int, outline: str, fill: str):
        canvas.create_oval(x-r, y-r, x+r, y+r, outline=outline, fill=fill)
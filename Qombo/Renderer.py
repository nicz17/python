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
from ProgressBar import *

class Renderer:
    """Rendering methods for Qombo."""
    iRadiusGrid = 36
    iRadiusSel  = 64
    selpos: Position

    log = logging.getLogger('Renderer')

    def __init__(self, grid: Grid, canGrid: tk.Canvas, canSelection: tk.Canvas, iSize: int):
        self.iSize = iSize
        self.grid = grid
        self.canGrid = canGrid
        self.canSelection = canSelection
        self.fontBold = tkfont.Font(family="Helvetica", size=12, weight='bold')
        self.iHeight = self.grid.h*self.iSize
        self.iWidth  = self.grid.w*self.iSize
        self.selpos = None
        self.child = None
        self.aHighlightIds = []
        self.progressBar = ProgressBar(grid.size())
        
        # Add image dir if missing
        if not os.path.exists(Qombit.sImageDir):
            os.makedirs(Qombit.sImageDir)

    def drawGrid(self):
        """Draw grid lines and qombits on the grid canvas"""
        self.canGrid.delete('all')
        self.aHighlightIds = []
        self.drawGridLines()
        for x in range(self.grid.w):
            for y in range(self.grid.h):
                qombit = self.grid.get(x, y)
                self.drawQombit(x, y, qombit)
        if self.getSelectedQombit() is not None:
            self.drawHighlight(self.selpos, 'yellow')
        self.drawGridProgress()

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

    def drawGridProgress(self):
        """Draw a progress bar showing grid fill"""
        px, py = 10, self.iHeight - 35
        self.progressBar.setAt(self.grid.count())
        self.canSelection.create_rectangle(px, py, px+180, py+25, fill=self.progressBar.getColor())
        self.canSelection.create_text(px+90, py+12, text = 'Board ' + self.progressBar.getTextPercent() + ' full')

    def drawSelection(self, pos: Position):
        """Update the selection canvas"""
        self.canSelection.delete('all')
        self.selpos = pos
        qombit = self.getSelectedQombit()
        if qombit:
            tx, ty = 100, 120
            self.canSelection.create_text(tx, 20, text = qombit.sName, font = self.fontBold)
            self.canSelection.create_image(tx-80, ty-80, anchor = tk.NW, image = qombit.getImageLarge())
            self.canSelection.create_text(tx, 220, text = str(qombit.oRarity) + ' ' + str(qombit.oKind))
            self.canSelection.create_text(tx, 240, text = 'Level ' + str(qombit.iLevel))
            self.canSelection.create_text(tx, 300, text = qombit.getDescription())
            if qombit.canGenerate():
                self.canSelection.create_text(tx, 400, text = 'Generates', font = self.fontBold)
                self.child = Qombit('Sample', qombit.getGeneratedKind(), 1, OrRarity.Common)
                self.canSelection.create_image(tx-50, 420, anchor = tk.NW, image = self.child.getImage())
                self.canSelection.create_text(tx, 540, text = qombit.getGeneratedKind().name + ' level 1')
            elif qombit.oKind == OrKind.Objective:
                self.canSelection.create_text(tx, 400, text = 'Target', font = self.fontBold)
                self.child = qombit.oTarget
                self.canSelection.create_image(tx-50, 420, anchor = tk.NW, image = self.child.getImage())
                self.canSelection.create_text(tx, 540, text = qombit.getTargetDescription())
            else:
                self.child = None
        else:
            self.canSelection.create_text(100, 20, text = 'Ready')
        self.drawGridProgress()

    def drawHighlight(self, pos: Position, color: str):
        """Draw a highlight square at the specified grid position."""
        #self.log.info('Highlight at %s', pos)
        if pos:
            w = 3
            x0 = pos.x * self.iSize + 1
            y0 = pos.y * self.iSize + 1
            x1 = x0 + self.iSize - w
            y1 = y0 + self.iSize - w
            self.aHighlightIds.append(self.canGrid.create_line(x0, y0, x1, y0, fill=color, width=w))
            self.aHighlightIds.append(self.canGrid.create_line(x0, y0, x0, y1, fill=color, width=w))
            self.aHighlightIds.append(self.canGrid.create_line(x0, y1, x1, y1, fill=color, width=w))
            self.aHighlightIds.append(self.canGrid.create_line(x1, y0, x1, y1, fill=color, width=w))

    def hideHighlights(self):
        """Hide the highlights on the grid canvas."""
        for id in self.aHighlightIds:
            self.canGrid.itemconfigure(id, state='hidden')

    def drawCircle(self, canvas: tk.Canvas, x:int, y: int, r: int, outline: str, fill: str):
        canvas.create_oval(x-r, y-r, x+r, y+r, outline=outline, fill=fill)

    def getSelectedQombit(self) -> Qombit:
        if self.selpos:
            return self.grid.get(self.selpos.x, self.selpos.y)
        return None
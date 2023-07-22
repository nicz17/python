"""
 Rendering methods for Motus.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
from tkinter import font as tkfont
import logging
from BaseApp import *
from Grid import *
from Guess import *

class Renderer:
    """Rendering methods for Motus."""
    colorGridLines = '#b0e0e0'
    log = logging.getLogger('Renderer')

    def __init__(self, grid: Grid, canGrid: tk.Canvas, iSize: int, root: tk.Tk):
        #self.fontBold = tkfont.Font(family="Helvetica", size=12, weight='bold')
        self.fontGuess = tkfont.Font(family="Helvetica", size=32, weight='normal')
        self.iSize = iSize
        self.grid = grid
        self.root = root
        self.canGrid = canGrid
        self.iHeight = self.grid.h*self.iSize
        self.iWidth  = self.grid.w*self.iSize

    def drawGuess(self, guess: Guess):
        """Draw the specified word guess on the grid canvas."""
        self.log.info('Rendering guess %s', guess)
        ty = self.iSize/2
        for x in range(guess.size()):
            tx = self.iSize/2 + x*self.iSize
            self.canGrid.create_text(tx, ty, text = guess.word[x].upper(), font = self.fontGuess)

    def drawGrid(self):
        """Draw grid lines and guesses on the grid canvas"""
        self.canGrid.delete('all')
        self.drawGridLines()

    def drawGridLines(self):
        """Draw lines on the grid canvas"""
        for x in range(self.grid.w):
            gx = x*self.iSize
            gy = self.iHeight
            self.canGrid.create_line(gx, 0, gx, gy, fill=self.colorGridLines, width=1)
        for y in range(self.grid.h):
            gx = self.iWidth
            gy = y*self.iSize
            self.canGrid.create_line(0, gy, gx, gy, fill=self.colorGridLines, width=1)
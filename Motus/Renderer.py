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
from Guess import *

class Renderer:
    """Rendering methods for Motus."""
    colorGridLines = '#b0e0e0'
    log = logging.getLogger('Renderer')

    def __init__(self, gridW: int, gridH: int, canGrid: tk.Canvas, iSize: int, root: tk.Tk):
        #self.fontBold = tkfont.Font(family="Helvetica", size=12, weight='bold')
        self.fontGuess = tkfont.Font(family="Helvetica", size=36, weight='bold')
        self.iSize = iSize
        self.gridW = gridW
        self.gridH = gridH
        self.root = root
        self.canGrid = canGrid
        self.iHeight = self.gridH*self.iSize
        self.iWidth  = self.gridW*self.iSize

    def drawGuesses(self, guesses):
        """Draw the specified word guesses on the grid canvas."""
        self.drawGrid()
        y = 0
        for guess in guesses:
            self.drawGuess(guess, y)
            y += 1

    def drawGuess(self, guess: Guess, y: int):
        """Draw the specified word guess on the grid canvas."""
        self.log.info('Rendering guess %s', guess)
        sy = y*self.iSize
        ty = sy + self.iSize/2 + 5
        for x in range(guess.size()):
            sx = x*self.iSize
            tx = sx + self.iSize/2
            letter = guess.letters[x]
            color = self.getColor(letter)
            self.canGrid.create_rectangle(sx+10, sy+10, sx+self.iSize-10, sy+self.iSize-10, fill=color, outline='')
            self.canGrid.create_text(tx, ty, text = letter.char, font = self.fontGuess, fill='white')

    def getColor(self, letter: Letter):
        """Returns the rendering color for the letter status."""
        if letter.status == LetterStatus.Correct:
            return '#10ff20'
        if letter.status == LetterStatus.Close:
            return '#f0f010'
        if letter.status == LetterStatus.Wrong:
            return '#101010'
        if letter.status == LetterStatus.Pending:
            return '#a0a0a0'
        if letter.status == LetterStatus.Invalid:
            return '#f01010'

    def drawGrid(self):
        """Draw grid lines and guesses on the grid canvas"""
        self.canGrid.delete('all')
        self.drawGridLines()

    def drawGridLines(self):
        """Draw lines on the grid canvas"""
        for x in range(self.gridW):
            gx = x*self.iSize
            gy = self.iHeight
            self.canGrid.create_line(gx, 0, gx, gy, fill=self.colorGridLines, width=1)
        for y in range(self.gridH):
            gx = self.iWidth
            gy = y*self.iSize
            self.canGrid.create_line(0, gy, gx, gy, fill=self.colorGridLines, width=1)
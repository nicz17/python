"""
 Qombo App window based on BaseApp.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
from tkinter import ttk
import logging
from BaseApp import *
from Grid import *
from Qombit import *
from Palette import *
from Timer import *

class QomboApp(BaseApp):
    """Qombo App window."""
    log = logging.getLogger('QomboApp')
    iSize = 100
    gridW = 8
    gridH = 6

    def __init__(self, sGeometry = '1100x650') -> None:
        self.iHeight = self.gridH*self.iSize
        self.iWidth  = self.gridW*self.iSize
        self.grid = Grid(self.gridW, self.gridH)
        self.qombitGen = QombitGen(42)
        super().__init__('Qombo', sGeometry)

    def generate(self):
        self.log.info('Generating Qombits')
        for x in range(self.gridW):
            for y in range(self.gridH):
                qombit = self.qombitGen.generate()
                self.grid.put(x, y, qombit)
                self.drawQombit(x, y, qombit)
    
    def onGridClick(self, event):
        """Handle grid click event."""
        self.log.info('Grid clicked at %d:%d', event.x, event.y)
        gx = int(event.x/self.iSize)
        gy = int(event.y/self.iSize)
        self.setStatus('Select cell ' + str(gx) + ':' + str(gy) + ' ' + self.grid.valueAsStr(gx, gy))

    def drawQombit(self, x, y, qombit: Qombit):
        """Draw the Qombit on the grid canvas."""
        r = 36
        tx = x*self.iSize + 50
        ty = y*self.iSize + 50
        self.canGrid.create_oval(tx-r, ty-r, tx+r, ty+r, outline='#a0d0d0', fill=qombit.getColor())
        self.canGrid.create_text(tx, ty, text=qombit.oKind)


    def drawGrid(self):
        for x in range(self.gridW):
            gx = x*self.iSize
            gy = self.iHeight
            self.canGrid.create_line(gx, 0, gx, gy, fill="#b0e0e0", width=1)
        for y in range(self.gridH):
            gx = self.iWidth
            gy = y*self.iSize
            self.canGrid.create_line(0, gy, gx, gy, fill="#b0e0e0", width=1)

    def createWidgets(self):
        """Create user widgets"""
        self.addButton('New Game', self.generate)

        #self.frmMain.configure(bg='black')
        self.canGrid = tk.Canvas(master=self.frmMain, bg='#c0f0f0', bd=0, 
                                    height=self.iHeight, width=self.iWidth, highlightthickness=0)
        self.canGrid.pack(side=tk.LEFT)
        self.canGrid.bind("<Button-1>", self.onGridClick)
        self.frmSelection = tk.Frame(master=self.frmMain, bg='#f0f0c0', bd=0, 
                                    height=self.iHeight, width=200, highlightthickness=0)
        self.frmSelection.pack(side=tk.RIGHT)
        #tk.Label(master=self.frmSelection, text='Selection', height=2).pack(side=tk.TOP)
        self.drawGrid()

    def addButton(self, sText, fnCmd):
        """Add a button with the specified label and callback."""
        btn = tk.Button(master=self.frmButtons, text=sText, command=fnCmd)
        btn.pack(fill=tk.X, padx=4, pady=2)

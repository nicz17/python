"""
 Qombo App window based on BaseApp.
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
from Timer import *

class QomboApp(BaseApp):
    """Qombo App window."""
    log = logging.getLogger('QomboApp')
    selection: Qombit
    iSize = 100
    gridW = 8
    gridH = 6

    def __init__(self, sGeometry = '1120x650') -> None:
        self.iHeight = self.gridH*self.iSize
        self.iWidth  = self.gridW*self.iSize
        self.grid = Grid(self.gridW, self.gridH)
        self.qombitGen = QombitGen(42)
        self.selection = None
        super().__init__('Qombo', sGeometry)
        self.fontBold = tkfont.Font(family="Helvetica", size=12, weight='bold')
        self.enableWidgets()

    def generate(self):
        """Generate new game state"""
        self.log.info('Generating Qombits')
        for x in range(self.gridW):
            for y in range(self.gridH):
                qombit = self.qombitGen.generate()
                self.grid.put(x, y, qombit)
                self.drawQombit(x, y, qombit)
        self.drawSelection()
        self.enableWidgets()

    def sellQombit(self):
        """Sells the selected qombit."""
        self.setStatus('Selling')
    
    def onGridClick(self, event):
        """Handle grid click event."""
        self.log.info('Grid clicked at %d:%d', event.x, event.y)
        gx = int(event.x/self.iSize)
        gy = int(event.y/self.iSize)
        #self.setStatus('Select cell ' + str(gx) + ':' + str(gy) + ' ' + self.grid.valueAsStr(gx, gy))
        qombit = self.grid.get(gx, gy)
        self.selection = qombit
        self.enableWidgets()
        self.drawSelection()

    def drawQombit(self, x, y, qombit: Qombit):
        """Draw the Qombit on the grid canvas."""
        if qombit:
            r = 36
            tx = x*self.iSize + 50
            ty = y*self.iSize + 50
            self.canGrid.create_oval(tx-r, ty-r, tx+r, ty+r, outline='#a0d0d0', fill=qombit.getColor())
            self.canGrid.create_text(tx, ty, text = qombit.oKind)

    def drawSelection(self):
        """Update the selection canvas"""
        self.canSelection.delete('all')
        if self.selection:
            qombit = self.selection
            self.canSelection.create_text(100, 20, text = qombit.sName, font = self.fontBold)
            r = 64
            tx = 100
            ty = 120
            self.canSelection.create_oval(tx-r, ty-r, tx+r, ty+r, outline='#a0d0d0', fill=qombit.getColor())
            self.canSelection.create_text(100, 220, text = str(qombit.oRarity) + ' ' + str(qombit.oKind))
            self.canSelection.create_text(100, 240, text = 'Level ' + str(qombit.iLevel))
        else:
            self.canSelection.create_text(100, 20, text = 'Ready')

    def drawGrid(self):
        """Draw lines on the grid canvas"""
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
        self.btnGenerate = self.addButton('New Game', self.generate)
        self.btnSell     = self.addButton('Sell', self.sellQombit)

        #self.frmMain.configure(bg='black')
        self.canGrid = tk.Canvas(master=self.frmMain, bg='#c0f0f0', bd=0, 
                                    height=self.iHeight, width=self.iWidth, highlightthickness=0)
        self.canGrid.pack(side=tk.LEFT)
        self.canGrid.bind("<Button-1>", self.onGridClick)
        self.canSelection = tk.Canvas(master=self.frmMain, bg='#f0f0c0', bd=0, 
                                    height=self.iHeight, width=200, highlightthickness=0)
        self.canSelection.pack(side=tk.RIGHT)
        self.drawGrid()

    def addButton(self, sLabel: str, fnCmd):
        """Add a button with the specified label and callback."""
        btn = tk.Button(master=self.frmButtons, text=sLabel, command=fnCmd)
        btn.pack(fill=tk.X, padx=4, pady=2)
        return btn
    
    def enableWidgets(self):
        """Enable or disable buttons based on state"""
        self.enableButton(self.btnGenerate, self.grid.isEmpty())
        self.enableButton(self.btnSell, self.selection is not None)
        
    def enableButton(self, btn, bEnabled: bool):
        """Enable the specified button if bEnabled is true."""
        if btn:
            if bEnabled:
                btn['state'] = tk.NORMAL
            else:
                btn['state'] = tk.DISABLED
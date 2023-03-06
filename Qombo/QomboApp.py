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
from Timer import *
from Renderer import *

class QomboApp(BaseApp):
    """Qombo App window."""
    log = logging.getLogger('QomboApp')
    selection: Qombit
    oDragFrom: Position
    grid: Grid
    iSize = 110
    gridW = 9
    gridH = 7

    def __init__(self, sGeometry = '1300x800') -> None:
        self.iHeight = self.gridH*self.iSize
        self.iWidth  = self.gridW*self.iSize
        self.grid = Grid(self.gridW, self.gridH)
        self.oDragFrom = None
        self.dragdroptag = None
        super().__init__('Qombo', sGeometry)
        self.renderer = Renderer(self.grid, self.canGrid, self.canSelection, self.iSize)
        self.renderer.drawGrid()
        self.setSelection(None)

    def newGame(self):
        """Generate new game state"""
        self.log.info('Starting new game')
        pos = self.grid.getCenter()
        if pos:
            qombit = GeneratorQombit(1, OrRarity.Common)
            x, y = pos.x, pos.y
            self.grid.put(x, y, qombit)
            self.renderer.drawQombit(x, y, qombit)
        self.setSelection(None)

    def generate(self):
        """Generate a new qombit if the selection is a generator."""
        if self.canGenerate():
            at = self.grid.find(self.selection)
            pos = self.grid.closestEmptyCell(at)
            if pos:
                qombit = self.selection.generate()
                x, y = pos.x, pos.y
                self.log.info('Generated %s at %s', qombit, pos)
                self.grid.put(x, y, qombit)
                self.enableWidgets()

    def canGenerate(self) -> bool:
        """Check if it is possible to generate a new qombit."""
        if self.selection:
            if self.selection.oKind == OrKind.Generator:
                return not self.grid.isFull()
        return False

    def sellQombit(self):
        """Sells the selected qombit."""
        if self.canSell():
            sold = self.grid.remove(self.selection)
            if sold:
                self.log.info('Sold %s', sold)
                self.setSelection(None)
                self.renderer.drawGrid()
                self.setStatus('Sold ' + str(sold))

    def canSell(self):
        """Check if it is possible to sell the current selection."""
        if self.selection:
            if self.selection.oKind == OrKind.Generator:
                return False
            return True
        return False
    
    def onGridClick(self, at: Position):
        """Handle grid click event."""
        self.log.info('Grid selection %s %s', at, self.grid.valueAsStr(at.x, at.y))
        qombit = self.grid.get(at.x, at.y)

        # Reselection
        if qombit and qombit == self.selection:
            if self.canGenerate():
                self.generate()
        # New selection
        else:
            self.setSelection(qombit)

        # Redraw grid in any case
        self.renderer.drawGrid()

    def onDragStart(self, event: tk.Event):
        self.oDragFrom = self.getGridPos(event.x, event.y)
        #self.log.info('Grid drag start %s %s', self.oDragFrom, self.grid.valueAsStr(self.oDragFrom.x, self.oDragFrom.y))
        self.canGrid.bind('<Motion>', self.onDragMove)
        self.canGrid.bind('<ButtonRelease-1>', self.onDragEnd)
        self.canGrid.addtag_withtag('dragdroptag', tk.CURRENT)

    def onDragMove(self, event: tk.Event):
        #x, y, r = event.x, event.y, self.renderer.iRadiusGrid
        #self.canGrid.coords('dragdroptag', x-r, y-r, x+r, y+r)
        x, y = event.x - 50, event.y - 50
        self.canGrid.coords('dragdroptag', x, y)

    def onDragEnd(self, event: tk.Event):
        oDragTo = self.getGridPos(event.x, event.y)
        #self.log.info('Grid drag end %s %s', oDragTo, self.grid.valueAsStr(oDragTo.x, oDragTo.y))
        self.canGrid.dtag('dragdroptag')    # removes the 'dragdroptag' tag
        self.canGrid.unbind('<Motion>')

        if oDragTo == self.oDragFrom:
            self.onGridClick(oDragTo)
        else:
            self.doDragDrop(self.oDragFrom, oDragTo)
        self.oDragFrom = None

    def doDragDrop(self, oFrom: Position, oTo: Position):
        qom1 = self.grid.get(oFrom.x, oFrom.y)
        qom2 = self.grid.get(oTo.x, oTo.y)
        if qom1 == qom2:
            # Combine
            self.log.info('Combining %s and %s', oFrom, oTo)
            qom1.combine()
            self.grid.put(oTo.x, oTo.y, qom1)
            self.grid.put(oFrom.x, oFrom.y, None)
        else:
            self.log.info('Swapping %s and %s', oFrom, oTo)
            self.grid.swap(oFrom, oTo)
        self.setSelection(qom1)
        self.renderer.drawGrid()

    def setSelection(self, qombit: Qombit):
        """Set the specified qombit as selected and update widgets"""
        self.selection = qombit
        self.renderer.drawSelection(self.selection)
        self.enableWidgets()

    def createWidgets(self):
        """Create user widgets"""
        self.btnStart = self.addButton('New Game', self.newGame)
        self.btnSell  = self.addButton('Sell', self.sellQombit)
        self.btnGen   = self.addButton('Generate', self.generate)

        self.canGrid = tk.Canvas(master=self.frmMain, bg='#c0f0f0', bd=0, 
                                    height=self.iHeight, width=self.iWidth, highlightthickness=0)
        self.canGrid.pack(side=tk.LEFT)
        self.canGrid.bind('<1>', self.onDragStart)
        self.canSelection = tk.Canvas(master=self.frmMain, bg='#f0f0c0', bd=0, 
                                    height=self.iHeight, width=200, highlightthickness=0)
        self.canSelection.pack(side=tk.RIGHT)

    def addButton(self, sLabel: str, fnCmd):
        """Add a button with the specified label and callback."""
        btn = tk.Button(master=self.frmButtons, text=sLabel, command=fnCmd)
        btn.pack(fill=tk.X, padx=4, pady=2)
        return btn
    
    def enableWidgets(self):
        """Enable or disable buttons based on state"""
        self.enableButton(self.btnStart, self.grid.isEmpty())
        self.enableButton(self.btnSell,  self.canSell())
        self.enableButton(self.btnGen,   self.canGenerate())
        
    def enableButton(self, btn: tk.Button, bEnabled: bool):
        """Enable the specified button if bEnabled is true."""
        if btn:
            if bEnabled:
                btn['state'] = tk.NORMAL
            else:
                btn['state'] = tk.DISABLED

    def getGridPos(self, x: int, y: int) -> Position:
        """Return the grid cell corresponding to the x,y grid canvas pixel"""
        gx = int(x/self.iSize)
        gy = int(y/self.iSize)
        return Position(gx, gy)
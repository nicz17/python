"""
 Qombo App window based on BaseApp.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
import logging
import getpass
from BaseApp import *
from DialogCollection import *
from Game import *
from GameSave import *
from Grid import *
from Qombit import *
from QombitFactory import *
from QombitCollection import *
from Timer import *
from Renderer import *
from HintProvider import *
import DateTools

class QomboApp(BaseApp):
    """Qombo App window."""
    log = logging.getLogger('QomboApp')
    selpos: Position
    oDragFrom: Position
    game: Game
    grid: Grid
    iSize = 110
    gridW = 9
    gridH = 7

    def __init__(self) -> None:
        self.iHeight = self.gridH*self.iSize
        self.iWidth  = self.gridW*self.iSize
        self.grid = Grid(self.gridW, self.gridH)
        self.oDragFrom = None
        self.dragdroptag = None
        sGeometry = str(self.iWidth + 320) + 'x' + str(self.iHeight + 30)
        super().__init__('Qombo', sGeometry)
        self.window.resizable(width=False, height=False)
        self.renderer = Renderer(self.grid, self.canGrid, self.canSelection, self.iSize, self.window)
        self.hintProvider = HintProvider(self.grid)
        self.game = None
        self.gameSave = GameSave()
        self.collec = QombitCollection()
        self.renderer.drawGrid()
        self.setSelection(None)

    def newGame(self):
        """Generate new game state"""
        self.log.info('Starting new game')
        sPlayer = getpass.getuser()
        self.game = Game(self.sTitle, sPlayer, 0)

        # First generator
        oGenerator = QombitFactory.fromValues('Premier', OrKind.Generator, 1, OrRarity.Common)
        self.grid.put(2, int(self.gridH/2), oGenerator)

        # First objective
        oObjective = QombitFactory.createObjective(0)
        self.grid.put(self.gridW-3, int(self.gridH/2), oObjective)
        
        self.renderer.drawGrid()
        self.setSelection(None)
        self.renderer.displayMessage('New game')

    def resumeGame(self):
        """Resume a saved game"""
        self.game = self.gameSave.load('autosave.json', self.grid)
        self.log.info('Resuming saved game %s', str(self.game))
        self.renderer.drawGrid()
        self.setSelection(None)
        self.setStatus('Welcome to ' + self.sTitle + ', ' + self.game.sPlayer + ' !')
        self.renderer.displayMessage(f'Welcome back, {self.game.sPlayer}!')

        # Populate collection from grid
        for pos in self.grid:
            self.collec.add(self.grid.getAt(pos))
    
    def saveGame(self):
        """Save the game state to json file."""
        if self.game is not None:
            self.gameSave.save('autosave.json', self.game, self.grid)

    def generate(self):
        """Generate a new qombit if the selection is a generator."""
        if self.canGenerate():
            pos = self.grid.closestEmptyCell(self.selpos)
            if pos:
                qombit = self.getSelectedQombit().generate()
                self.log.info('Generated %s at %s', qombit, pos)
                self.grid.put(pos.x, pos.y, qombit)
                self.enableWidgets()
                self.renderer.drawGrid()
                self.updateCollection(qombit)
        else:
            self.log.info('Cannot generate')

    def canGenerate(self) -> bool:
        """Check if it is possible to generate a new qombit."""
        qombit = self.getSelectedQombit()
        if qombit is not None and qombit.canGenerate():
            return not self.grid.isFull()
        return False

    def sellQombit(self):
        """Sells the selected qombit."""
        if self.canSell():
            sold = self.grid.remove(self.getSelectedQombit())
            if sold:
                iPoints = sold.getPoints()
                self.game.incScore(iPoints)
                self.log.info('Sold %s for %d points', sold, iPoints)
                self.setSelection(None)
                self.renderer.drawGrid()
                self.setStatus('Sold ' + str(sold))

    def canSell(self):
        """Check if it is possible to sell the current selection."""
        qombit = self.getSelectedQombit()
        if qombit is not None:
            return qombit.canSell()
        return False
    
    def objectiveComplete(self, oObjective: ObjectiveQombit, oTarget: Qombit):
        """Check if the objective is completed."""
        if oObjective is not None and oObjective.oTarget == oTarget:
            nPoints = oObjective.getPoints()
            self.log.info('Objective %s completed', oObjective)
            self.game.incProgress()
            self.game.incScore(nPoints)
            posNext = self.grid.closestEmptyCell(self.grid.getCenter())
            self.grid.remove(oObjective)
            self.grid.remove(oTarget)
            self.addObjective(posNext)
            self.setSelection(None)
            self.renderer.drawGrid()
            self.renderer.displayMessage(f'+ {nPoints} points!')
            return True
        return False
    
    def addObjective(self, pos: Position):
        """Add a new objective."""
        if not self.grid.isFull():
            #pos = self.grid.closestEmptyCell(self.grid.getCenter())
            assert(pos is not None)
            obj = QombitFactory.createObjective(self.game.iProgress)
            self.grid.put(pos.x, pos.y, obj)
            self.setStatus('New objective: ' + str(obj))
    
    def onGridClick(self, at: Position):
        """Handle grid click event."""
        self.log.info('Grid selection %s %s', at, self.grid.valueAsStr(at.x, at.y))

        # Reselection
        if at is not None and at == self.selpos:
            #self.log.info('Reselection at %s', str(at))
            if self.canGenerate():
                self.generate()
            else:
                self.renderer.drawGrid()
        # New selection
        else:
            #self.log.info('New selection at %s', str(at))
            self.setSelection(at)
            self.renderer.drawGrid()

        # Redraw grid in any case
        #self.renderer.drawGrid()

    def onDragStart(self, event: tk.Event):
        self.oDragFrom = self.getGridPos(event.x, event.y)
        #self.log.info('Grid drag start %s %s', self.oDragFrom, self.grid.valueAsStr(self.oDragFrom.x, self.oDragFrom.y))
        self.canGrid.bind('<Motion>', self.onDragMove)
        self.canGrid.bind('<ButtonRelease-1>', self.onDragEnd)
        self.canGrid.addtag_withtag('dragdroptag', tk.CURRENT)

    def onDragMove(self, event: tk.Event):
        self.renderer.moveQombit(event.x, event.y)

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
        if not oTo in self.grid:
            self.log.error('Cannot drop at %s', oTo)
            self.renderer.drawGrid()
            return
        qom1 = self.grid.getAt(oFrom)
        qom2 = self.grid.getAt(oTo)
        bSwap = True
        if qom1 is None and qom2 is None:
            return
        if qom1 == qom2:
            # Combine TODO put in dedicated method
            self.log.info('Combining %s and %s', oFrom, oTo)
            qom1.evolve()
            self.grid.put(oTo.x, oTo.y, qom1)
            self.grid.put(oFrom.x, oFrom.y, None)
            bSwap = False
            self.setSelection(oTo)
            self.renderer.drawGrid()
            self.updateCollection(qom1)
        elif qom2 and qom2.oKind == OrKind.Objective:
            # Check if objective is complete
            bSwap = not self.objectiveComplete(qom2, qom1)

        if bSwap:
            self.log.info('Swapping %s and %s', oFrom, oTo)
            self.grid.swap(oFrom, oTo)
            self.setSelection(oTo)
            self.renderer.drawGrid()

    def setSelection(self, pos: Position):
        """Set the specified position as selected and update widgets"""
        self.selpos = pos
        self.renderer.drawSelection(pos)
        self.enableWidgets()
        self.updateScore()

    def getSelectedQombit(self) -> Qombit:
        """Get the Qombit at the selected grid cell."""
        if self.selpos:
            return self.grid.get(self.selpos.x, self.selpos.y)
        return None
    
    def updateScore(self):
        """Display the current game score."""
        sScore = 'No Score'
        if self.game is not None:
            sScore = 'Score: ' + str(self.game.iScore)
        self.lblScore.configure(text = sScore)

    def getHint(self):
        """Display a hint on what to do next."""
        hint = self.hintProvider.getHint()
        if hint is not None:
            self.setStatus('Hint: ' + hint.sText)
            for pos in hint:
                self.renderer.drawHighlight(pos, 'red')
            self.renderer.displayMessage(hint.sText)

    def updateCollection(self, qombit: Qombit):
        """Add the qombit to the collection. Gain points if it is new."""
        if qombit is not None and not qombit in self.collec:
            self.collec.add(QombitFactory.copy(qombit))
            self.renderer.displayMessage('Collection expanded!')
            self.game.incScore(1)
            self.updateScore()

    def showCollection(self):
        """Display the current qombit collection in a modal window."""
        self.collec.dump()
        dlgCollect = DialogCollection(self.window, self.collec)
        self.log.info('Opened dialog window, waiting')
        dlgCollect.displayKind(OrKind.Star)
        self.window.wait_window(dlgCollect.root)
        self.log.info(f'Dialog closed with data: {dlgCollect.data}')

    def displayGameInfo(self, event):
        """Display a message-box with game info."""
        sMsg = 'Game not started yet.'
        if self.game:
            sStart = DateTools.timestampToString(self.game.tStart, "%d.%m.%Y %H:%M:%S")
            sMsg = self.game.sName + '\n'
            sMsg += f'Player {self.game.sPlayer}\n'
            sMsg += f'Score {self.game.iScore}\n'
            sMsg += f'Started {sStart}\n'
            sMsg += f'Objectives completed: {self.game.iProgress}\n'
        messagebox.showinfo(title='Game Info', message=sMsg)

    def onBeforeClose(self):
        self.saveGame()

    def onKeyHint(self, event):
        self.getHint()

    def onKeyGenerate(self, event):
        if self.canGenerate():
            self.generate()
            self.renderer.drawGrid()
        else:
            hint = self.hintProvider.findGenerator()
            if hint is not None:
                self.setSelection(hint.aPositions[0])
                self.generate()
                self.renderer.drawGrid()

    def onKeyMerge(self, event):
        pair = self.hintProvider.findPair()
        if pair is not None:
            self.doDragDrop(pair.aPositions[0], pair.aPositions[1])

    def createWidgets(self):
        """Create user widgets"""

        # Buttons
        self.btnStart  = self.addButton('New Game', self.newGame)
        self.btnResume = self.addButton('Resume', self.resumeGame)
        self.btnSell   = self.addButton('Sell', self.sellQombit)
        self.btnSave   = self.addButton('Save', self.saveGame)
        self.btnHint   = self.addButton('Hint', self.getHint)
        self.btnCollec = self.addButton('Collection', self.showCollection)

        # Score label
        self.lblScore = tk.Label(self.frmButtons, text='Score: 0')
        self.lblScore.pack(fill=tk.X, pady=6)
        self.lblScore.bind('<1>', self.displayGameInfo)

        # Canvas
        self.canGrid = tk.Canvas(master=self.frmMain, bg='#c0f0f0', bd=0, 
                                    height=self.iHeight, width=self.iWidth, highlightthickness=0)
        self.canGrid.pack(side=tk.LEFT)
        self.canGrid.bind('<1>', self.onDragStart)
        self.canSelection = tk.Canvas(master=self.frmMain, bg='#f0f0c0', bd=0, 
                                    height=self.iHeight, width=200, highlightthickness=0)
        self.canSelection.pack(side=tk.RIGHT)

        # Keyboard shortcuts
        self.window.bind('h', self.onKeyHint)
        self.window.bind('g', self.onKeyGenerate)
        self.window.bind('m', self.onKeyMerge)
    
    def enableWidgets(self):
        """Enable or disable buttons based on state"""
        self.enableButton(self.btnStart,  self.grid.isEmpty())
        self.enableButton(self.btnResume, self.grid.isEmpty())
        self.enableButton(self.btnSell,   self.canSell())
        self.enableButton(self.btnSave,   not self.grid.isEmpty())
        self.enableButton(self.btnHint,   not self.grid.isEmpty())
        
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
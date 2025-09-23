#!/usr/bin/env python3

"""
 GUI for the Game of Life
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import logging
import tkinter as tk

from BaseApp import *
from gameOfLife import GameOfLife, SeedGenerator, State


class LifeGrig():
    """Canvas to display game state."""
    log = logging.getLogger('LifeGrid')
    cellw = 40

    def __init__(self, parent, size):
        """Constructor"""
        self.parent = parent
        self.size = size
        self.cells = []

    def render(self, state: State):
        """Render the state."""
        if state is None:
            return
        for x in range(state.getSize()[0]):
            for y in range(state.getSize()[1]):
                isAlive = state.getCell(x, y)
                cell = self.cells[self.getCellId(x, y)]
                self.canvas.itemconfigure(cell, fill=('green' if isAlive else 'black'))

    def createWidgets(self):
        """Create user widgets."""

        # Canvas
        width  = self.cellw*self.size[0] +1
        height = self.cellw*self.size[1] +1
        self.canvas = tk.Canvas(self.parent, width=width, height=height, bg='blue')
        self.canvas.pack(pady=10)

        # Cell squares
        for y in range(self.size[1]):
            yr = y*self.cellw +1
            for x in range(self.size[0]):
                xr = x*self.cellw +1
                id = self.canvas.create_rectangle(xr, yr, xr + self.cellw-1, yr + self.cellw-1, fill='red')
                self.cells.append(id)

    def getCellId(self, x: int, y: int) -> int:
        """Get cell Id from x, y coords."""
        return x + self.size[0]*y

    def __str__(self):
        return 'LifeGrid'

class LifeViewApp(BaseApp):
    """Game of Life app window."""
    log = logging.getLogger('LifeViewApp')
    size = (24, 18)
    density = 0.12
    maxTicks = 100
    interval = 800

    def __init__(self) -> None:
        """Constructor."""
        self.iWidth  = 1200
        self.iHeight =  800
        geometry = f'{self.iWidth + 120}x{self.iHeight + 40}'
        super().__init__('Life Viewer', geometry)
        self.window.resizable(width=False, height=False)
        self.setupGame()
        self.isRunning = False

    def setupGame(self):
        """Create a new game."""
        self.gen = SeedGenerator(self.size)
        self.game = GameOfLife('RandomGame', self.gen.random(self.density))
        self.log.info(self.game)
        #self.log.info(self.game.state)
        self.grid.render(self.game.state)

    def onReset(self):
        """Reset the game seed."""
        self.game.setSeed(self.gen.random(self.density))
        self.grid.render(self.game.state)

    def onRunGame(self):
        """Run or stop the game."""
        if self.isRunning:
            self.log.info(f'Stopping {self.game} after {self.tick} ticks')
            self.isRunning = False
        else:
            self.log.info(f'Running {self.game}')
            self.isRunning = True
            self.tick = 0
            self.tickDisplay()

    def onSave(self):
        """Save the game seed to a json file."""
        self.game.toJsonFile()

    def tickDisplay(self):
        """Display the next tick."""
        self.tick += 1
        if self.tick > self.maxTicks:
            self.isRunning = False

        if self.isRunning:
            #self.log.info(f'Rendering tick {self.tick}')
            self.game.evolve()
            self.grid.render(self.game.state)
            self.window.after(self.interval, self.tickDisplay)

            if self.game.state.countAlive() == 0:
                self.isRunning = False
        else:
            self.log.info('Done.')

    def createWidgets(self):
        """Create user widgets."""
        self.log.info('Creating App widgets')
        self.grid = LifeGrig(self.frmMain, self.size)
        self.grid.createWidgets()

        self.btnRun   = self.addButton('Run',   self.onRunGame)
        self.btnReset = self.addButton('Reset', self.onReset)
        self.btnSave  = self.addButton('Save',  self.onSave)

    def __str__(self):
        return 'LifeViewApp'


def configureLogging():
    """Configures logging to have timestamped logs at INFO level."""
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
        level=logging.INFO, datefmt = '%Y.%m.%d %H:%M:%S',
        handlers=[logging.StreamHandler()])
    return logging.getLogger('lifeViewer')

def main():
    """Main routine."""
    log.info('Welcome to LifeViewer v' + __version__)
    app = LifeViewApp()
    app.run()
    
log = configureLogging()
main()
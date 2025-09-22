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
        pass

    def createWidgets(self):
        """Create user widgets."""

        # Canvas
        width = self.cellw*self.size[0]
        self.canvas = tk.Canvas(self.parent, width=width, height=width, bg='black')
        self.canvas.pack()

        # Cell squares
        for x in range(self.size[0]):
            xr = x*self.cellw
            for y in range(self.size[1]):
                yr = y*self.cellw
                id = self.canvas.create_rectangle(xr, yr, xr + self.cellw-1, yr + self.cellw-1, fill='red')
                self.cells.append(id)

    def __str__(self):
        return 'LifeGrid'

class LifeViewApp(BaseApp):
    """Game of Life app window."""
    log = logging.getLogger('LifeViewApp')
    size = (16, 16)

    def __init__(self) -> None:
        """Constructor."""
        self.iWidth  = 1200
        self.iHeight =  800
        geometry = f'{self.iWidth + 120}x{self.iHeight + 40}'
        super().__init__('Life Viewer', geometry)
        self.window.resizable(width=False, height=False)
        self.setupGame()

    def setupGame(self):
        """Create a new game."""
        gen = SeedGenerator(self.size)
        self.game = GameOfLife('RandomGame', gen.random(0.15))
        self.log.info(self.game)
        self.grid.render(self.game.state)

    def createWidgets(self):
        """Create user widgets."""
        self.log.info('Creating App widgets')
        self.grid = LifeGrig(self.frmMain, self.size)
        self.grid.createWidgets()

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
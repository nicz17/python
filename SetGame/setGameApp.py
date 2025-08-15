#!/usr/bin/env python3

"""
 GUI for the Set card game
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import logging

from BaseApp import *
from game import Game
from playmat import Playmat


class SetGameApp(BaseApp):
    """Set game app window."""
    log = logging.getLogger('SetGameApp')

    def __init__(self) -> None:
        self.iWidth  = 1500
        self.iHeight =  980
        self.game = None
        self.dragdroptag = None
        self.playmat = Playmat(self.iWidth, self.iHeight)
        sGeometry = str(self.iWidth + 320) + 'x' + str(self.iHeight + 30)
        super().__init__('Set', sGeometry)
        self.window.resizable(width=False, height=False)

    def onSetPlayers(self):
        pass

    def onNewGame(self):
        """Start a new game."""
        if self.game is None:
            self.game = Game()
            self.game.createDeck()
            self.game.shuffle()
            cards = self.game.deal(12)
            self.playmat.addCards(cards)

    def createWidgets(self):
        """Create user widgets."""

        # Buttons
        self.btnPlayers = self.addButton('Joueurs', self.onSetPlayers)
        self.btnStart   = self.addButton('Nouvelle partie', self.onNewGame)

        # Playmat
        self.playmat.createWidgets(self.frmMain)
        self.playmat.render()

        # Auto-start game
        self.onNewGame()


def configureLogging():
    """Configures logging to have timestamped logs at INFO level."""
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
        level=logging.INFO,
        datefmt = '%Y.%m.%d %H:%M:%S',
        handlers=[logging.StreamHandler()])
    return logging.getLogger('Cassino')

def main():
    """Main routine."""
    log.info('Welcome to Set game v' + __version__)
    app = SetGameApp()
    app.run()
    
log = configureLogging()
main()

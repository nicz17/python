#!/usr/bin/env python3

"""
 GUI for the Set card game
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import logging

from BaseApp import *
from card import Card
from game import Game
from playmat import Playmat


class SetGameApp(BaseApp):
    """Set game app window."""
    log = logging.getLogger('SetGameApp')

    def __init__(self) -> None:
        """Constructor."""
        self.iWidth  = 1500
        self.iHeight =  980
        self.game = None
        self.activeCards = []
        self.selectedCards = []
        self.playmat = Playmat(self.iWidth, self.iHeight, self.onCardSelection)
        sGeometry = str(self.iWidth + 320) + 'x' + str(self.iHeight + 30)
        super().__init__('Set', sGeometry)
        self.window.resizable(width=False, height=False)

    def onSetPlayers(self):
        pass

    def onNewGame(self):
        """Start a new game."""
        self.activeCards = []
        self.game = Game()
        self.game.createDeck()
        self.game.shuffle()
        cards = self.game.deal(12)
        for card in cards:
            self.activeCards.append(card)
        self.selectedCards = []
        self.playmat.reset()
        self.playmat.addCards(cards)

    def onCardSelection(self, card: Card):
        """Card selection callback."""
        if card:
            self.selectedCards.append(card)
            self.validateSet()

    def validateSet(self):
        """Validate the selected card set."""
        if len(self.selectedCards) == 3:
            isSet = self.game.isSet(self.selectedCards)
            if isSet:
                self.showInfoMsg("Bravo, c'est un set !")
                self.replaceSetCards()
            else:
                self.showErrorMsg("Ce n'est pas un set.")
            self.selectedCards = []
            self.playmat.deleteHighlights()

    def replaceSetCards(self):
        """Replace 3 cards on playmat after a valid set was found."""
        for card in self.selectedCards:
            self.activeCards.remove(card)
        repl = self.game.deal(3)
        for card in repl:
            self.activeCards.append(card)
        self.playmat.reset()
        self.playmat.addCards(self.activeCards)

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

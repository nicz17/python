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
from game import Game, InvalidSetReason
from player import Player
from playmat import Playmat
from Timer import Timer

class SetGameApp(BaseApp):
    """Set game app window."""
    log = logging.getLogger('SetGameApp')

    def __init__(self) -> None:
        """Constructor."""
        self.iWidth  = 1600
        self.iHeight =  980
        self.timer = Timer()
        self.game = None
        self.activeCards = []
        self.selectedCards = []
        self.players = []
        self.playmat = Playmat(self.iWidth, self.iHeight, self.onCardSelection)
        sGeometry = f'{self.iWidth + 220}x{self.iHeight + 30}'
        super().__init__('Set', sGeometry)
        self.window.resizable(width=False, height=False)

    def onSetPlayers(self):
        """Display player config dialog."""
        # TODO implement player config dialog
        self.players.append(Player('Esti', '#ff69b4'))
        self.players.append(Player('Nicz', '#add8f6'))
        self.playmat.addPlayers(self.players)

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
        self.playmat.addCards(cards)
        self.updatePlaymat()
        self.timer.start()

    def onCardSelection(self, card: Card):
        """Card selection callback."""
        if card:
            self.selectedCards.append(card)
            self.validateSet()

    def onHint(self):
        """Hint button callback."""
        # TODO highlight hint card
        # TODO if no sets, reshuffle and deal again
        nSets = self.game.findSets(self.activeCards)
        msg = "Il n'y a pas de set." 
        if nSets == 1: msg = f'Il y a {nSets} set.'
        if nSets >= 2: msg = f'Il y a {nSets} sets.'
        self.showInfoMsg(msg)

    def validateSet(self):
        """Validate the selected card set."""
        # TODO implement set validation dialog
        if len(self.selectedCards) == 3:
            isSet = self.game.isSet(self.selectedCards)
            if isSet:
                self.timer.stop()
                self.log.info('Found valid set')
                self.showInfoMsg(f"Bravo, c'est un set !\nTrouvé en {self.timer.getElapsed()}")
                self.replaceSetCards()
            else:
                self.log.info('Selection is not a set')
                kind = self.game.getInvalidSetReason(self.selectedCards)
                reason = self.explainInvalidSet(kind)
                self.showErrorMsg(f"Ce n'est pas un set :\n{reason}.")
            self.selectedCards = []
            self.playmat.deleteHighlights()

    def explainInvalidSet(self, kind: InvalidSetReason) -> str:
        """Explain why the selected cards don't form a set."""
        if kind == InvalidSetReason.InvalidShapes:
            return 'les formes ne sont pas toutes identiques ou toutes différentes'
        if kind == InvalidSetReason.InvalidNumbers: 
            return 'les nombres ne sont pas tous identiques ou tous différents'
        if kind == InvalidSetReason.InvalidColors:
            return 'les couleurs ne sont pas toutes identiques ou toutes différentes'
        if kind == InvalidSetReason.InvalidFills:
            return 'les remplissages ne sont pas tous identiques ou tous différents'
        return kind

    def replaceSetCards(self):
        """Replace 3 cards on playmat after a valid set was found."""
        # TODO detect game over: empty deck, no sets on playmat
        for card in self.selectedCards:
            self.activeCards.remove(card)
        repl = self.game.deal(3)
        for card in repl:
            self.activeCards.append(card)
        self.playmat.addCards(self.activeCards)
        self.updatePlaymat()
        self.timer.start()

    def updatePlaymat(self):
        """Update the playmat with the current game state."""
        self.playmat.updateState(self.game.getDeckCount())

    def createWidgets(self):
        """Create user widgets."""

        # Buttons
        self.btnPlayers = self.addButton('Joueurs', self.onSetPlayers)
        self.btnStart   = self.addButton('Nouvelle partie', self.onNewGame)
        self.btnHint    = self.addButton('Indice', self.onHint)

        # Playmat
        self.playmat.createWidgets(self.frmMain)
        self.playmat.render()

        # Auto-start game
        self.onSetPlayers()
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

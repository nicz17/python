#!/usr/bin/env python3

"""
 GUI for the Set card game
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import logging
import random

from BaseApp import *
from card import Card
from game import Game, CardSet, InvalidSetReason
from player import Player
from playmat import Playmat, MessageBox
from Timer import Timer
import TextTools

class SetGameApp(BaseApp):
    """Set game app window."""
    log = logging.getLogger('SetGameApp')

    def __init__(self) -> None:
        """Constructor."""
        self.iWidth  = 1700
        self.iHeight =  980
        self.timer = Timer()
        self.game = None
        self.activeCards = []
        self.selectedCards = []
        self.players = []
        self.activePlayer = None
        self.hintAvailable = True
        self.fBestTime = 60.0
        self.playmat = Playmat(self.iWidth, self.iHeight, 
                self.onCardSelection, self.onPlayerSelection)
        sGeometry = f'{self.iWidth + 120}x{self.iHeight + 30}'
        # TODO ajouter icone
        super().__init__('Set', sGeometry)
        self.window.resizable(width=False, height=False)

    def onSetPlayers(self):
        """Display player config dialog."""
        # TODO implement player config dialog

    def onSetDefaultPlayers(self):
        """Display default players."""
        self.players.append(Player('Esti', '#ff69b4'))
        self.players.append(Player('Nicz', '#add8f6'))
        self.playmat.addPlayers(self.players)

    def onNewGame(self):
        """Start a new game."""
        self.activeCards = []
        for player in self.players:
            player.score = 0
        self.fBestTime = 60.0
        self.game = Game()
        self.game.createDeck()
        self.game.shuffle()
        cards = self.game.deal(12)
        for card in cards:
            self.activeCards.append(card)
        self.selectedCards = []
        self.playmat.resetMessageBoard()
        self.playmat.addCards(cards)
        self.playmat.addMessage(MessageBox('La partie commence !', None))
        self.updatePlaymat()
        self.enableWidgets()
        self.timer.start()

    def onGameOver(self):
        """Game is over."""
        self.log.info('Game over!')
        self.playmat.addMessage(MessageBox('La partie est terminée !', None))

    def onCardSelection(self, card: Card):
        """Card selection callback."""
        if card is None:
            return
        if card in self.selectedCards:
            self.log.info(f'Card is already selected, unselecting')
            self.selectedCards.remove(card)
            self.playmat.unselectCard(card)
        else:
            self.selectedCards.append(card)
            self.validateSet()

    def onPlayerSelection(self, player: Player):
        """Player selection callback."""
        if player is None:
            return
        self.activePlayer = player
        # TODO unselect player
        self.log.info(f'Active player: {player}')

    def onHint(self):
        """Hint button callback."""
        sets = self.game.findSets(self.activeCards)
        nSets = len(sets)
        if nSets == 0 and self.game.getDeckCount() == 0:
            # Game over, hint should be disabled
            self.log.error('Game over, no hint available!')
            return
        if nSets == 0:
            self.reshuffleAndDeal()
        else:
            msg = f'Indice : il y a {nSets} set{"s" if nSets>1 else ""}'
            cardSet = random.choice(sets)
            hint = cardSet.getRandomCard()
            self.log.info(f'Hint: {hint}')
            self.playmat.displayHint(hint)
            self.playmat.addMessage(MessageBox(msg, None))
            self.hintAvailable = False
        self.enableWidgets()

    def validateSet(self):
        """Validate the selected card set."""
        # TODO implement set validation dialog
        if len(self.selectedCards) == 3:
            isSet = self.game.isSet(self.selectedCards)
            if isSet:
                # Time to find the set
                self.timer.stop()
                tFound = self.timer.getElapsedSeconds()
                sTime = TextTools.durationToString(tFound)

                # Update player score
                self.log.info(f'Valid set found by {self.activePlayer}')
                if self.activePlayer:
                    self.activePlayer.addScore(3)
                self.playmat.addMessage(MessageBox(f'a trouvé un set en {sTime}', self.activePlayer))

                # Check best time record
                if tFound < self.fBestTime:
                    self.fBestTime = tFound
                    self.playmat.addMessage(MessageBox(f'a battu le record en {sTime}', self.activePlayer))

                # Update game state
                self.showInfoMsg(f"Bravo, c'est un set !\nTrouvé en {sTime}")
                self.replaceSetCards()
                self.hintAvailable = True
                self.playmat.highlightPlayer(None)
            else:
                self.log.info('Selection is not a set')
                kind = self.game.getInvalidSetReason(self.selectedCards)
                reason = self.explainInvalidSet(kind)
                self.showErrorMsg(f"Ce n'est pas un set :\n{reason}.")
            self.selectedCards = []
            self.playmat.deleteHighlights()
            self.enableWidgets()

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
        for card in self.selectedCards:
            self.activeCards.remove(card)
        if self.game.getDeckCount() == 0:
            nSets = self.game.countSets(self.activeCards)
            if nSets == 0:
                self.onGameOver()
        else:
            repl = self.game.deal(3)
            for card in repl:
                self.activeCards.append(card)
        self.playmat.addCards(self.activeCards)
        self.updatePlaymat()
        self.timer.start()

    def reshuffleAndDeal(self):
        """If no more sets, reshuffle and deal again."""
        self.log.info('No more sets on playmat, will reshuffle')
        msg = "Il n'y a pas de set.\nLes cartes vont être remélangées." 
        self.showInfoMsg(msg)

        # Shuffle active cards back into deck and deal 12
        for card in self.activeCards:
            self.game.cards.append(card)
        self.game.shuffle()
        self.activeCards = self.game.deal(12)
        self.selectedCards = []

        # Update playmat
        self.playmat.reset()
        self.playmat.addCards(self.activeCards)
        self.updatePlaymat()
        self.playmat.addMessage(MessageBox('Pas de set, nouvelle donne', None))
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
        self.onSetDefaultPlayers()
        self.onNewGame()

    def enableWidgets(self):
        """Enable or diasable the game buttons."""
        # TODO add game status enum
        self.enableButton(self.btnHint, self.hintAvailable)


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

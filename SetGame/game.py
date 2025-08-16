"""
The Set game.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import logging
import random

from card import Card, CardColor, CardFill, CardShape

class Game():
    """The Set game."""
    log = logging.getLogger('SetGame')

    def __init__(self):
        """Constructor."""
        self.log.info('Welcome to the Set game!')
        self.cards = []

    def createDeck(self):
        """Create the deck of 81 cards."""
        self.log.info('Creating the deck.')
        self.cards = []

        for shape in CardShape:
            for color in CardColor:
                for fill in CardFill:
                    for number in range(3):
                        card = Card(color, shape, fill, number+1)
                        self.cards.append(card)

        self.log.info(f'Generated {len(self.cards)} cards')

    def shuffle(self):
        """Shuffle the cards."""
        random.shuffle(self.cards)

    def deal(self, amount: int) -> list[Card]:
        """Deal an amount of cards."""
        self.log.info(f'Dealing {amount} cards')
        result = []
        for i in range(amount):
            if len(self.cards) > 0:
                result.append(self.cards.pop(0))
        return result

    def isSet(self, cards: list[Card]) -> bool:
        """Check if the cards form a valid set."""
        if cards is None:
            return False
        if len(cards) != 3:
            return False
        
        setNums = set(card.number for card in cards)
        if len(setNums) == 2:
            self.log.info('Invalid numbers')
            return False
        setShapes = set(card.shape for card in cards)
        if len(setShapes) == 2:
            self.log.info('Invalid shapes')
            return False
        setColors = set(card.color for card in cards)
        if len(setColors) == 2:
            self.log.info('Invalid colors')
            return False
        setFills = set(card.fill for card in cards)
        if len(setFills) == 2:
            self.log.info('Invalid fills')
            return False
        return True
    
    def getInvalidSetReason(self, cards: list[Card]) -> str:
        """Returns the reason why the cards don't form a set."""
        # TODO implement reason
        return 'Non'


def testIsSet(game: Game, cards: list[Card]):
    game.log.info('Testing isSet for:')
    for card in cards:
        game.log.info(card)
    isSet = game.isSet(cards)
    game.log.info('Valid set' if isSet else 'Not a set')

def testSetGame():
    game = Game()
    game.createDeck()
    game.shuffle()
    #game.deal(12)
    testIsSet(game, game.deal(3))

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testSetGame()
"""
The Set game.
"""

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
        #for card in self.cards:
        #    self.log.info(card)

    def shuffle(self):
        """Shuffle the cards."""
        random.shuffle(self.cards)

    def deal(self, amount: int):
        """Deal an amount of cards."""
        self.log.info(f'Dealing {amount} cards')
        dealt = self.cards[0:amount]
        for card in dealt:
            self.log.info(card)

def testSetGame():
    game = Game()
    game.createDeck()
    game.shuffle()
    game.deal(12)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testSetGame()
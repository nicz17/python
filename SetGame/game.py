"""
The Set game.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

from enum import Enum
import logging
import random

from card import Card, CardColor, CardFill, CardShape

class InvalidSetReason(Enum):
    """Enumeration of reasons why a set is not valid."""
    InvalidCardCount = 0,
    InvalidNumbers = 1,
    InvalidColors = 2,
    InvalidShapes = 3,
    InvalidFills = 4

class CardSet():
    """A valid set of 3 cards."""
    log = logging.getLogger('CardSet')

    def __init__(self, cards: list[Card]):
        """Constructor."""
        self.cards = cards

    def getRandomCard(self):
        """Return a card at random from this set."""
        return random.choice(self.cards)
    
    def getSortedCards(self):
        """Return the cards sorted."""
        return sorted(self.cards)

    def getScore(self):
        return 3

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

    def getDeckCount(self) -> int:
        """Count cards left in deck."""
        return len(self.cards)

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
            return False
        setShapes = set(card.shape for card in cards)
        if len(setShapes) == 2:
            return False
        setColors = set(card.color for card in cards)
        if len(setColors) == 2:
            return False
        setFills = set(card.fill for card in cards)
        if len(setFills) == 2:
            return False
        return True
    
    def getInvalidSetReason(self, cards: list[Card]) -> InvalidSetReason:
        """Returns the reason why the cards don't form a set."""
        if len(cards) != 3:
            return InvalidSetReason.InvalidCardCount
        setNums = set(card.number for card in cards)
        if len(setNums) == 2:
            return InvalidSetReason.InvalidNumbers
        setShapes = set(card.shape for card in cards)
        if len(setShapes) == 2:
            return InvalidSetReason.InvalidShapes
        setColors = set(card.color for card in cards)
        if len(setColors) == 2:
            return InvalidSetReason.InvalidColors
        setFills = set(card.fill for card in cards)
        if len(setFills) == 2:
            return InvalidSetReason.InvalidFills
        return None
    
    def findSets(self, cards: list[Card]) -> int:
        """Look for sets and return number of sets found."""
        self.log.info(f'Looking for sets among {len(cards)} cards')
        count = 0
        for i, c1 in enumerate(cards[0:-2]):
            for j, c2 in enumerate(cards[i+1:-1]):
                for c3 in cards[i+j+2:]:
                    if self.isSet([c1, c2, c3]):
                        count += 1
                        self.log.info(f'Set {c1.toShortStr()} {c2.toShortStr()} {c3.toShortStr()}')
        self.log.info(f'Found {count} sets')
        return count
    
    def computeStats(self):
        """Evaluate how often there is at least one set in a deal of 12 cards."""
        n = 10000
        noSets = 0
        for i in range(n):
            self.createDeck()
            self.shuffle()
            cards = self.deal(12)
            count = self.findSets(cards)
            if count == 0:
                noSets += 1
        self.log.info(f'Prob of no set in 12 cards: {(noSets/n):.3f} from {n} tries')
        # Result is 3.4%

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
    #testIsSet(game, game.deal(3))
    cards = game.deal(12)
    game.findSets(cards)
    #game.computeStats()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testSetGame()
"""Module for the Cassino game."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import random
from enum import Enum


class Suit(Enum):
    """Enumeration of card suits."""
    Spades   = 0
    Hearts   = 1
    Clubs    = 2
    Diamonds = 3

    def getName(self) -> str:
        """Getter for french name."""
        match self:
            case Suit.Spades:   return 'pique'
            case Suit.Hearts:   return 'coeur'
            case Suit.Clubs:    return 'trèfle'
            case Suit.Diamonds: return 'carreau'

    def getColor(self) -> str:
        """Getter for color."""
        match self:
            case Suit.Spades:   return '#000000'
            case Suit.Hearts:   return '#ff0000'
            case Suit.Clubs:    return '#000000'
            case Suit.Diamonds: return '#ff0000'

    def __str__(self):
        return self.name


class Card():
    """Class Card"""
    log = logging.getLogger("Card")

    def __init__(self, value: int, suit: Suit):
        """Constructor."""
        self.value = value
        self.suit = suit

    def getName(self) -> str:
        """Getter for french name."""
        svalue = str(self.value)
        match self.value:
            case 1:  svalue = 'As'
            case 11: svalue = 'Valet'
            case 12: svalue = 'Dame'
            case 13: svalue = 'Roi'
        return f'{svalue} de {self.suit.getName()}'

    def getValue(self) -> int:
        """Getter for value"""
        return self.value

    def getSuit(self) -> Suit:
        """Getter for suit"""
        return self.suit
        
    def __eq__(self, other): 
        if not isinstance(other, Card):
            return NotImplemented
        return self.value == other.value and self.suit.value == other.suit.value

    def toJson(self):
        """Create a dict of this Card for json export."""
        data = {
            'value': self.value,
            'suit':  self.suit
        }
        return data

    def __str__(self):
        return f'{self.value}{self.suit.name}'


class Deck():
    """Class Deck"""
    log = logging.getLogger("Deck")

    def __init__(self):
        """Constructor."""
        self.cards = []
        for suit in Suit:
            for value in range(13):
                self.cards.append(Card(value+1, suit))
        self.shuffle()

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def deal(self, amount: int) -> list[Card]:
        """Deal the specified amount of cards."""
        result = []
        for i in range(amount):
            if len(self.cards) > 0:
                result.append(self.cards.pop(0))
        return result

    def toJson(self):
        """Create a dict of this Deck for json export."""
        data = {
            'cards': self.cards,
        }
        return data

    def __str__(self):
        return f'Deck of {len(self.cards)} cards'


class Trick():
    """Class Trick"""
    log = logging.getLogger("Trick")
    greaterCassino = Card(10, Suit.Diamonds)
    lesserCassino  = Card( 2, Suit.Spades)

    def __init__(self):
        """Constructor."""
        self.cards = []

    def addCard(self, card: Card):
        """Add a card."""
        if card:
            self.cards.append(card)

    def getCards(self) -> list[Card]:
        return self.cards

    def size(self) -> int:
        """Size."""
        return len(self.cards)

    def getScore(self) -> int:
        """Count the score of this trick."""
        score = 0
        if self.size() > 26:
            score += 1
        nSpades = 0
        for card in self.getCards():
            if card.suit == Suit.Spades:
                nSpades += 1
            if card == self.greaterCassino:
                score += 1
            if card == self.lesserCassino:
                score += 1
            if card.value == 1:
                score += 1
        if nSpades > 6:
            score += 1
        return score

    def toJson(self):
        """Create a dict of this Trick for json export."""
        data = {
            'cards': self.cards
        }
        return data

    def __str__(self):
        return f'Trick of {len(self.cards)} cards'

def testTrick():
    """Unit test for Trick"""
    Trick.log.info("Testing Trick")
    deck = Deck()
    deck.log.info(deck)
    trick = Trick()
    for card in deck.deal(12):
        trick.addCard(card)
    trick.log.info(trick)
    for card in trick.getCards():
        trick.log.info(card.getName())
    trick.log.info('Score: %d', trick.getScore())
    deck.log.info(deck)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testTrick()

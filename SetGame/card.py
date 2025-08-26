"""
Cards for the Set game.
Cards have 3 colors, shapes, fills and numbers.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

from enum import Enum

class CardColor(Enum):
    """Enumeration of card colors."""
    Red = 0,
    Green = 1,
    Blue = 2

    def __str__(self):
        return f'CardColor {self.name}'
    
class CardShape(Enum):
    """Enumeration of card shapes."""
    Rect = 0,
    Oval = 1,
    Wave = 2

    def __str__(self):
        return f'CardShape {self.name}'
    
class CardFill(Enum):
    """Enumeration of card fillings."""
    Empty = 0,
    Hashed = 1,
    Full = 2

    def __str__(self):
        return f'CardFill {self.name}'

class Card():
    """A card of the Set game."""

    def __init__(self, color: CardColor, shape: CardShape, fill: CardFill, number: int):
        """Constructor with card values."""
        self.color = color
        self.shape = shape
        self.fill = fill
        self.number = number

    def getImageFilename(self) -> str:
        """Get the file name for this card image."""
        return f'{self.shape.name}{self.color.name}{self.fill.name}{self.number}.png'

    def toShortStr(self):
        """Returns a compact 4-letter string representation of this card."""
        return f'{self.shape.name[0]}{self.number}{self.color.name[0]}{self.fill.name[0]}'

    def __str__(self):
        return f'Card {self.number} {self.shape.name} {self.color.name} {self.fill.name}'
        

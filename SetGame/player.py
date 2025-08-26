"""Module for Srt game player."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import logging


class Player():
    """Class Player"""
    log = logging.getLogger("Player")

    def __init__(self, name: str, color: str):
        """Constructor."""
        self.name = name
        self.color = color
        self.score = 0
        self.image = f"images/meeple{name}.png"

    def getName(self) -> str:
        """Getter for name"""
        return self.name
    
    def getColor(self) -> str:
        """Getter for icon color."""
        return self.color

    def getScore(self) -> int:
        """Getter for score"""
        return self.score

    def addScore(self, points: int):
        """Add points to score."""
        self.score += points

    def getImage(self) -> str:
        """Getter for image filename."""
        return self.image

    def toJson(self):
        """Create a dict of this Player for json export."""
        data = {
            'name': self.name,
            'score': self.score,
            'image': self.image,
        }
        return data

    def __str__(self):
        str = f'Player {self.name} score {self.score}'
        return str


def testPlayer():
    """Unit test for Player"""
    Player.log.info("Testing Player")
    obj = Player('TestPlayer1')
    obj.log.info(obj)
    obj.log.info(obj.getName())

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testPlayer()

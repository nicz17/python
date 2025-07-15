"""Module SpaceInvader"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2025 N. Zwahlen"
__version__ = "1.0.0"

import logging
import random


class SpaceInvader():
    """Class SpaceInvader"""
    log = logging.getLogger("SpaceInvader")

    def __init__(self, width: int, height: int, maxValue: float):
        """Constructor."""
        self.width = width
        self.height = height
        self.maxValue = maxValue
        self.cx = int(width/2)

    def generate(self):
        """Generate."""
        self.log.info(f'Generating around {self.cx}')
        for y in range(self.height):
            for x in range(self.cx+1):
                value = random.uniform(0.0, self.maxValue)
                self.applyValue(x, y, value)

    def applyValue(self, xs: int, y: int, value: float):
        """Apply value."""
        x = self.cx - xs
        self.log.info(f'Value at [{x}:{y}] {value}')
        x = self.cx + xs
        self.log.info(f'Value at [{x}:{y}] {value}')

    def __str__(self):
        str = f'SpaceInvader {self.width}x{self.height} maxValue: {self.maxValue}'
        return str


def testSpaceInvader():
    """Unit test for SpaceInvader"""
    SpaceInvader.log.info("Testing SpaceInvader")
    obj = SpaceInvader(9, 6, 100.0)
    obj.log.info(obj)
    obj.generate()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testSpaceInvader()

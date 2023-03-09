"""
Provide hints for game progression.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
from Grid import *
from Qombit import *

class HintProvider():
    log = logging.getLogger(__name__)

    def __init__(self, grid: Grid) -> None:
        self.grid = grid

    def getHint(self) -> Position:
        return self.findGenerator()
    
    def findPair(self):
        pass

    def findGenerator(self) -> Position:
        for x in range(self.grid.w):
            for y in range(self.grid.h):
                qombit = self.grid.get(x, y)
                if qombit is not None and qombit.oKind == OrKind.Generator:
                    pos = Position(x, y)
                    self.log.info('Hint: use generator at %s', pos)
                    return pos
        return None
"""
Provide hints for game progression.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
from Grid import *
from Qombit import *

class Hint():
    """A list of grid positions and an explanation."""
    def __init__(self, sText) -> None:
        self.sText = sText
        self.aPositions = []

    def addPosition(self, pos: Position):
        self.aPositions.append(pos)

class HintProvider():
    """
    Provide hints for game progression.
    First look if there is a completed objective.
    Otherwise, find a pair of identical qombos to merge.
    Otherwise, find the best generator.
    """
    
    log = logging.getLogger(__name__)

    def __init__(self, grid: Grid) -> None:
        self.grid = grid

    def getHint(self) -> Hint:
        """Look for a hint on what to do next."""
        hint = self.findFinishedObjective()
        if hint is None:
            hint = self.findPair()
        if hint is None:
            hint = self.findGenerator()
        return hint
    
    def findFinishedObjective(self) -> Hint:
        """Look for a finished objective."""
        return None
    
    def findPair(self) -> Hint:
        """Look for a pair to combine."""
        for x in range(self.grid.w):
            for y in range(self.grid.h):
                qombit = self.grid.get(x, y)
                if qombit is not None and qombit.canEvolve():
                    pos1 = Position(x, y)
                    pos2 = self.findOther(qombit, pos1)
                    if pos2 is not None:
                        hint = Hint('Combine ' + str(qombit))
                        hint.addPosition(pos1)
                        hint.addPosition(pos2)
                        return hint
        return None
    
    def findOther(self, qombit: Qombit, pos: Position):
        """Find another qombit to combine with this one"""
        for x in range(self.grid.w):
            for y in range(self.grid.h):
                at = Position(x, y)
                if at != pos:
                    qombit2 = self.grid.get(x, y)
                    if qombit2 is not None and qombit2 == qombit:
                        return at
        return None

    def findGenerator(self) -> Hint:
        """Look for the most advanced generator on the grid."""
        hint = None
        iBestGen = -1
        for x in range(self.grid.w):
            for y in range(self.grid.h):
                qombit = self.grid.get(x, y)
                if qombit is not None and qombit.canGenerate():
                    if qombit.oKind.value > iBestGen:
                        iBestGen = qombit.oKind.value
                        hint = Hint('Generate more objects!')
                        hint.addPosition(Position(x, y))
        return hint
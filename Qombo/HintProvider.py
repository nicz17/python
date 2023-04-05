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
    Otherwise, find a pair of identical qombits to merge.
    Otherwise, find the best generator.
    """
    
    log = logging.getLogger(__name__)

    def __init__(self, grid: Grid) -> None:
        self.grid = grid

    def getHint(self) -> Hint:
        """Look for a hint on what to do next."""
        hint = self.findCompletedObjective()
        if hint is None:
            hint = self.findPair()
        if hint is None:
            hint = self.findGenerator()
        return hint
    
    def findCompletedObjective(self) -> Hint:
        """Look for a completed objective."""
        for pos in self.grid:
            qombit = self.grid.getAt(pos)
            if qombit and qombit.oKind == OrKind.Objective:
                pos2 = self.findOther(qombit.oTarget, pos)
                if pos2 is not None:
                    hint = Hint('Complete objective!')
                    hint.addPosition(pos)
                    hint.addPosition(pos2)
                    return hint
        return None
    
    def findPair(self) -> Hint:
        """Look for a pair to combine."""
        for pos in self.grid:
            qombit = self.grid.getAt(pos)
            if qombit is not None and qombit.canEvolve():
                pos2 = self.findOther(qombit, pos)
                if pos2 is not None:
                    hint = Hint('Combine identical objects!')
                    hint.addPosition(pos)
                    hint.addPosition(pos2)
                    return hint
        return None
    
    def findOther(self, qombit: Qombit, pos: Position):
        """Find another qombit to combine with this one."""
        for at in self.grid:
            if at != pos:
                qombit2 = self.grid.getAt(at)
                if qombit2 is not None and qombit2 == qombit:
                    return at
        return None

    def findGenerator(self) -> Hint:
        """Look for the most advanced generator on the grid."""
        hint = None
        iBestGen = -1
        for pos in self.grid:
            qombit = self.grid.getAt(pos)
            if qombit is not None and qombit.canGenerate():
                if qombit.oKind.value > iBestGen:
                    iBestGen = qombit.oKind.value
                    hint = Hint('Generate more objects!')
                    hint.addPosition(pos)
        return hint
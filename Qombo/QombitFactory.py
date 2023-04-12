"""
Create Qombits of various kinds.
Also handle creating Qombits from JSON.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
import random
from Qombit import *
from NameGen import *

class QombitFactory():
    log = logging.getLogger(__name__)
    nameGen = NameGen()

    @staticmethod
    def fromValues(sName: str, oKind: OrKind, iLevel: int, oRarity: OrRarity) -> Qombit:
        """Creates a new Qombit from the specified values."""
        qombit = Qombit(sName, oKind, iLevel, oRarity)
        if oKind == OrKind.Generator:
            #qombit = GeneratorQombit(sName, oKind, iLevel, oRarity)
            pass
        elif oKind == OrKind.Objective:
            #qombit = ObjectiveQombit(sName, oKind, iLevel, oRarity)
            pass
        return qombit

    @staticmethod
    def fromJson(oData: dict) -> Qombit:
        """Creates a new Qombit from the specified dict."""
        oKind = OrKind[oData['kind']]
        oRarity = OrRarity[oData['rarity']]
        qombit = Qombit(oData['name'], oKind, oData['level'], oRarity)
        if oKind == OrKind.Objective:
            oTarget = QombitFactory.fromJson(oData['target'])
            qombit = ObjectiveQombit(oData['name'], oData['level'], oRarity, oTarget)
        return qombit
    
    @staticmethod
    def createObjective(iDifficulty: int) -> ObjectiveQombit:
        """Creates a random objective"""
        QombitFactory.log.info('Creating an Objective with difficulty %d', iDifficulty)
        iObjectiveLevel = (iDifficulty % 4) + 1
        oObjectiveRarity = OrRarity((iDifficulty // 4) % 4)
        iTargetLevel = random.randint(2, min(6, iObjectiveLevel+2))
        oTargetKind = OrKind(1 + ((iDifficulty // 12) % 6))
        oRarity = oObjectiveRarity
        
        oTarget = Qombit('Target', oTargetKind, iTargetLevel, oRarity)
        oObjective = ObjectiveQombit(QombitFactory.nameGen.generate(), iObjectiveLevel, oObjectiveRarity, oTarget)
        return oObjective
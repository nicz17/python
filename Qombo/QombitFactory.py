"""
Create Qombits of various kinds.
Also handle creating Qombits from JSON.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
from Qombit import *

class QombitFactory():
    log = logging.getLogger(__name__)

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
    def objective() -> ObjectiveQombit:
        """Creates a random objective"""
        oTarget = Qombit('Target', OrKind.Star, 5, OrRarity.Common)
        oObjective = ObjectiveQombit('Goal', 1, OrRarity.Common, oTarget)
        return oObjective
"""
 An artifact with a name, kind and rarity
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

from enum import Enum
import random

class OrKind(Enum):
    Food = 0
    Source = 1
    Duplicator = 2
    Combiner = 3
    Objective = 4

    def __str__(self):
        return self.name

class OrRarity(Enum):
    Common  = 0
    Unusual = 1
    Rare    = 2
    Mythic  = 3

    @staticmethod
    def random():
        return random.choices(list(OrRarity), OrRarity.weights())[0]

    @staticmethod
    def weights():
        return [81, 27, 9, 1]

    def __str__(self):
        return self.name

class Ortifact:
    def __init__(self, sName, oKind, iLevel, oRarity):
        self.sName = sName
        self.oKind = oKind
        self.iLevel = iLevel
        self.oRarity = oRarity

    def __str__(self):
        return self.sName + ' is a level ' + str(self.iLevel) + ' ' + str(self.oRarity) + ' ' + str(self.oKind)
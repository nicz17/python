from enum import Enum

class OrKind(Enum):
    Food = 0
    Source = 1
    Duplicator = 2
    Combiner = 3

    def __str__(self):
        return self.name

class OrRarity(Enum):
    Common = 0
    Uncommon = 1
    Rare = 2
    Mythic = 3

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
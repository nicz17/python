from enum import Enum

class OrKind(Enum):
    Food = 0
    Source = 1
    Duplicator = 2
    Combiner = 3

    def __str__(self):
        return self.name

class Ortifact:
    def __init__(self, sName, oKind, iLevel, iRarity):
        self.sName = sName
        self.oKind = oKind
        self.iLevel = iLevel
        self.iRarity = iRarity

    def __str__(self):
        return self.sName + ' is a level ' + str(self.iLevel) + ' ' + str(self.oKind)
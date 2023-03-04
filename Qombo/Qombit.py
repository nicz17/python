"""
 An artifact with a name, kind and rarity
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

from enum import Enum
import random
from NameGen import *

class OrKind(Enum):
    Generator  = 0
    Food       = 1
    Duplicator = 2
    Objective  = 3

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

class Qombit:
    """An item that can be combined with another to make a better item"""
    aColors = ['#c0c0c0', '#a0a0ff', 'yellow', 'orange']

    def __init__(self, sName: str, oKind: OrKind, iLevel: int, oRarity: OrRarity):
        self.sName = sName
        self.oKind = oKind
        self.iLevel = iLevel
        self.oRarity = oRarity

    def getColor(self):
        """Get this Qombit's color based on its rarity."""
        return self.aColors[self.oRarity.value]

    def generate(self):
        """Generate a new Qombit. Most Qombits can't do this."""
        return None

    def __str__(self):
        return self.sName + ' level ' + str(self.iLevel) + ' ' + str(self.oRarity) + ' ' + str(self.oKind)
    
class GeneratorQombit(Qombit):
    """A Qombit that can generate other Qombits"""

    def __init__(self, sName: str, iLevel: int, oRarity: OrRarity):
        super().__init__(sName, OrKind.Generator, iLevel, oRarity)
        self.nameGen = NameGen(42)
        self.generatedKind = OrKind.Food

    def getColor(self):
        return '#a0f0a0'

    def generate(self):
        """Generate a new Qombit."""
        sName = self.nameGen.generate()
        iLevel = 1
        qombit = Qombit(sName, self.generatedKind, iLevel, OrRarity.random())
        return qombit
    
class QombitGen:
    def __init__(self, seed):
        self.seed = seed
        self.nameGen = NameGen(seed)

    def generate(self, oKind = None):
        sName = self.nameGen.generate()
        if oKind is None:
            oKind = random.choice(list(OrKind))
        iLevel = random.randrange(6)
        qombit = Qombit(sName, oKind, iLevel, OrRarity.random())
        return qombit
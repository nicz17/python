"""
 An artifact with a name, kind and rarity
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

from enum import Enum
import random
from NameGen import *
from Palette import *

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
    #aColors = ['#c0c0c0', '#a0a0ff', 'yellow', 'orange']

    def __init__(self, sName: str, oKind: OrKind, iLevel: int, oRarity: OrRarity):
        self.sName = sName
        self.oKind = oKind
        self.iLevel = iLevel
        self.oRarity = oRarity
        self.oPalette = HeatPalette()

    def getColor(self):
        """Get this Qombit's color based on its rarity and level."""
        rValue = 0.25*self.oRarity.value + 0.04*(self.iLevel-1)
        return self.oPalette.getColorHex(rValue)
        #return self.aColors[self.oRarity.value]
    
    def combine(self):
        """Result of combining this qombit with another one."""
        self.iLevel += 1

    def generate(self):
        """Generate a new Qombit. Most Qombits can't do this."""
        return None
    
    def getDescription(self) -> str:
        """Get a short text describing what to do with this qombit."""
        return 'Combine with an \nidentical object to \nupgrade level'

    def __str__(self):
        return self.sName + ' level ' + str(self.iLevel) + ' ' + str(self.oRarity) + ' ' + str(self.oKind)
        
    def __eq__(self, other): 
        if not isinstance(other, Qombit):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.oKind.value == other.oKind.value and self.oRarity.value == other.oRarity.value and self.iLevel == other.iLevel
    
class GeneratorQombit(Qombit):
    """A Qombit that can generate other Qombits"""

    def __init__(self, iLevel: int, oRarity: OrRarity):
        self.nameGen = NameGen(42)
        super().__init__(self.nameGen.generate(), OrKind.Generator, iLevel, oRarity)
        self.generatedKind = OrKind.Food
        self.aNames = []
        for i in range(4):
            self.aNames.append(self.nameGen.generate())

    def getColor(self):
        return 'yellow'

    def generate(self):
        """Generate a new Qombit."""
        iLevel = 1
        oRarity = OrRarity.random()
        sName = self.aNames[oRarity.value]
        qombit = Qombit(sName, self.generatedKind, iLevel, oRarity)
        return qombit
    
    def getDescription(self) -> str:
        return 'Click to create an object'
    
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
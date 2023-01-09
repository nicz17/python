"""
 A random artifact generator.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import random
from NameGen import *
from Ortifact import *

class OrtifactGen:
    def __init__(self, seed):
        self.seed = seed
        self.nameGen = NameGen(seed)

    def generate(self):
        sName = self.nameGen.generate()
        oKind = random.choice(list(OrKind))
        iLevel = random.randrange(6)
        ortifact = Ortifact(sName, oKind, iLevel, OrRarity.random())
        return ortifact

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
        iRarity = random.randrange(4)
        ortifact = Ortifact(sName, oKind, iLevel, iRarity)
        return ortifact

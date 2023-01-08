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
        oRarity = random.choice(list(OrRarity))
        iLevel = random.randrange(6)
        ortifact = Ortifact(sName, oKind, iLevel, oRarity)
        return ortifact

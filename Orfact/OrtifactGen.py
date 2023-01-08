import random
from NameGen import *
from Ortifact import *

class OrtifactGen:
    def __init__(self, seed):
        self.seed = seed
        self.nameGen = NameGen(seed)

    def generate(self):
        sName = self.nameGen.generate()
        iLevel = random.randrange(6)
        iRarity = random.randrange(4)
        ortifact = Ortifact(sName, iLevel, iRarity)
        return ortifact

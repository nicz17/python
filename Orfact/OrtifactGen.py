import random
from NameGen import *
from Ortifact import *

class OrtifactGen:
    def __init__(self, seed):
        self.seed = seed
        self.nameGen = NameGen(seed)
        self.kinds = ['Source', 'Food', 'Combiner', 'Duplicator']

    def generate(self):
        sName = self.nameGen.generate()
        sKind = random.choice(self.kinds)
        iLevel = random.randrange(6)
        iRarity = random.randrange(4)
        ortifact = Ortifact(sName, sKind, iLevel, iRarity)
        return ortifact

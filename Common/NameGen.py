"""
 A name generation tool.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.1"

import random

class NameGen:
    """A simple random name generator."""

    def __init__(self, seed=42, minSyl=2, maxSyl=4, flipProb=0.06):
        """Constructor with optional seed, min-amx syllables and syllable flip probability."""
        self.seed = seed
        self.minSyl = minSyl
        self.maxSyl = maxSyl
        self.flipProb = flipProb
        random.seed(seed)
        self.vowels = ['a', 'e', 'i', 'o', 'u', 'y']
        self.consos = ['b', 'c', 'd', 'f', 'g', 'h', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'x', 'z']

    def generate(self):
        """Generates and returns a random name."""
        nSyllables = random.randint(self.minSyl, self.maxSyl)
        sName = ''
        for s in range(nSyllables):
            sName += self.getSyllable()
        return sName.capitalize()

    def getSyllable(self):
        """Returns a random syllable."""
        rflip = random.random()
        if rflip < self.flipProb:
            return self.getVowel() + self.getConsonant()
        return self.getConsonant() + self.getVowel()

    def getVowel(self):
        """Returns a random vowel."""
        return random.choice(self.vowels)

    def getConsonant(self):
        """Returns a random consonant."""
        return random.choice(self.consos)

    def __str__(self):
        return f'NameGen seed {self.seed}, {self.minSyl}-{self.maxSyl} syllables, {self.flipProb} fliprate'


def testGrid(ng: NameGen):
    """Tests the name generator by printing several names to console."""
    nCols = 8
    nRows = 6
    print(ng)
    for iCol in range(nCols):
        sRow = ''
        for iRow in range(nRows):
            sName = ng.generate()
            sRow += sName.ljust(10)
        print(sRow)
    print()

def testNameGen():
    """Unit test for NameGen."""
    testGrid(NameGen(random.randint(0, 42)))
    testGrid(NameGen(random.randint(0, 42), 3, 3, 0.01))

if __name__ == '__main__':
    testNameGen()
"""
 A name generation tool
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import random

class NameGen:
    """A simple random name generator."""
    def __init__(self, seed = 42):
        self.seed = seed
        self.vowels = ['a', 'e', 'i', 'o', 'u', 'y']
        self.consos = ['b', 'c', 'd', 'f', 'g', 'h', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'x', 'z']

    def generate(self):
        """Generates and returns a random name."""
        nSyllables = random.randint(2, 4)
        sName = ''
        for s in range(nSyllables):
            sName += self.getSyllable()
        return sName.capitalize()

    def getSyllable(self):
        """Returns a random syllable."""
        rPermutation = random.random()
        if (rPermutation < 0.06):
            return self.getVowel() + self.getConsonant()
        elif (rPermutation < 0.12):
            self.getConsonant() + self.getConsonant() + self.getVowel()
        return self.getConsonant() + self.getVowel()

    def getVowel(self):
        """Returns a random vowel."""
        return random.choice(self.vowels)

    def getConsonant(self):
        """Returns a random consonant."""
        return random.choice(self.consos)

def testNameGen():
    """Tests the name generator by printing several names to console."""
    nCols = 8
    nRows = 6
    ng = NameGen()
    for iCol in range(nCols):
        sRow = ''
        for iRow in range(nRows):
            sName = ng.generate()
            sRow += sName.ljust(10)
        print(sRow)

if __name__ == '__main__':
    testNameGen()
"""
 A name generation tool
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import random

class NameGen:
    def __init__(self, seed):
        self.seed = seed
        self.vowels = ['a', 'e', 'i', 'o', 'u', 'y']
        self.consos = ['b', 'c', 'd', 'f', 'g', 'h', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'x', 'z']

    def generate(self):
        nSyllables = random.randint(2, 4)
        sName = ''
        for s in range(nSyllables):
            sName += self.getSyllable()
        return sName.capitalize()

    def getSyllable(self):
        rPermutation = random.random()
        if (rPermutation < 0.06):
            return self.getVowel() + self.getConsonant()
        elif (rPermutation < 0.12):
            self.getConsonant() + self.getConsonant() + self.getVowel()
        return self.getConsonant() + self.getVowel()

    def getVowel(self):
        return random.choice(self.vowels)

    def getConsonant(self):
        return random.choice(self.consos)


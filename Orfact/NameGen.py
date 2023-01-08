# Orfact NameGenerator

import random

class NameGen:
    def __init__(self, seed):
        self.seed = seed
        self.vowels = ['a', 'e', 'i', 'o', 'u', 'y']
        self.consos = ['b', 'c', 'd', 'f', 'g', 'h', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'z']

    def generate(self):
        nSyllables = random.randint(2, 4)
        sName = ''
        for s in range(nSyllables):
            sName += self.getSyllable()
        return sName.capitalize()

    def getSyllable(self):
        return self.getConsonant() + self.getVowel()

    def getVowel(self):
        return random.choice(self.vowels)

    def getConsonant(self):
        return random.choice(self.consos)


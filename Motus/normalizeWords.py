#!/usr/bin/env python3

"""
 A small word game inspired from Wordle, but in French.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import os
import logging
from FileReader import *


class Normalizer():
    """Motus word normalizer."""
    log = logging.getLogger('Normalizer')
    
    def __init__(self) -> None:
        """Constructor."""
        self.words = []
        self.getWords()

    def normalize(self):
        """Reformat the words input file."""
        self.log.info('Normalizing list of %d words', len(self.words))

        # Separate words by initial letter
        initial = None
        letterGroups = []
        letterGroup = []
        for word in self.words:
            if word[0] != initial:
                initial = word[0]
                letterGroup = []
                letterGroups.append(letterGroup)
            letterGroup.append(word)

        # Write new words file
        nWordsByRow = 15
        with open('words-norm.txt', 'w') as out:
            for letterGroup in letterGroups:
                wordCount = 0
                while wordCount < len(letterGroup):
                    line = letterGroup[wordCount : wordCount + nWordsByRow]
                    wordCount += nWordsByRow
                    out.write(' '.join(line))
                    out.write('\n')
                out.write('\n')

    def analyze(self):
        """Identify potential non-french words to remove."""

        # Find words containing suspicious letters
        susWords = []
        susLetters = ['K', 'W']
        for word in self.words:
            for letter in susLetters:
                if letter in word and not word[0] == letter:
                    susWords.append(word)

        # Display the suspicious words
        nWordsByRow = 8
        wordCount = 0
        self.log.info(f'Found {len(susWords)} suspicious words:')
        while wordCount < len(susWords):
            self.log.info(' '.join(susWords[wordCount : wordCount + nWordsByRow]))
            wordCount += nWordsByRow

    def getWords(self):
        """Build the list of valid 5-letter words."""
        
        # Parse words file
        filename = 'words.txt'
        self.log.info('Reading %s', filename)
        if not os.path.exists(filename):
            self.log.error('Missing words file %s, aborting', filename)
            exit('Abort')

        oFileReader = FileReader(filename)
        for line in oFileReader:
            for word in line.split(' '):
                if len(word) == 5:
                    self.words.append(word.upper())
                elif len(word) > 0:
                    self.log.error('Skipping invalid word [%s]', word)
        oFileReader.close()

        self.log.info('Built list of %d words', len(self.words))
    
def configureLogging():
    """
    Configures logging to have timestamped logs at INFO level
    on stdout and in a log file.
    """
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
        level=logging.INFO,
        datefmt = '%Y.%m.%d %H:%M:%S',
        handlers=[logging.StreamHandler()])
    return logging.getLogger('Motus')

def main():
    """Main routine."""
    log.info('Welcome to Motus Normalizer v' + __version__)
    norm = Normalizer()
    norm.analyze()
    norm.normalize()
    
log = configureLogging()
main()

"""
 Motus App window based on BaseApp.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
import logging
import random
from BaseApp import *

class MotusApp(BaseApp):
    """Motus App window."""
    log = logging.getLogger('MotusApp')

    def __init__(self) -> None:
        sGeometry = '1200x800'
        super().__init__('Motus', sGeometry)
        self.getWords()

    def newGame(self):
        """Start a new game with a random word."""
        self.log.info('New game started.')
        self.word = random.choice(self.words)
        self.log.info('Secret word is %s', self.word)

    def getWords(self):
        """Build the list of valid 5-letter words."""
        self.words = ['alors', 'beret', 'cacao', 'chaud', 'doses',
                      'etude', 'froid', 'glace', 'hibou', 'isole',
                      'jouer', 'livre', 'matou', 'nuits', 'offre',
                      'parti', 'queue', 'riens', 'savon', 'tuile',
                      'usage', 'voici', 'zones', 'radis', 'genou']
        self.log.info('Built list of %d words', len(self.words))

    def createWidgets(self):
        """Create user widgets"""

        # Buttons
        self.btnStart  = self.addButton('Démarrer', self.newGame)
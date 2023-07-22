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
from FileReader import *
from Guess import *
from Grid import *
from Renderer import *

class MotusApp(BaseApp):
    """Motus App window."""
    log = logging.getLogger('MotusApp')
    gridW = 5
    gridH = 6
    iSize = 110

    def __init__(self) -> None:
        self.iHeight = self.gridH*self.iSize
        self.iWidth  = self.gridW*self.iSize
        sGeometry = '1000x800'
        super().__init__('Motus', sGeometry)
        self.getWords()
        self.guess = Guess()
        self.grid = Grid(self.gridW, self.gridH)
        self.window.resizable(width=False, height=False)
        self.renderer = Renderer(self.grid, self.canGrid, self.iSize, self.window)
        self.newGame()

    def newGame(self):
        """Start a new game with a random word."""
        self.log.info('New game started.')
        self.word = random.choice(self.words)
        self.guess = Guess()
        self.log.info('Secret word is %s', self.word)
        self.renderer.drawGrid()

    def getWords(self):
        """Build the list of valid 5-letter words."""
        self.words = []
        
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

    def validateGuess(self):
        self.log.info('Validating guess %s', self.guess)
        if self.guess.isComplete():
            if not self.guess.word.upper() in self.words:
                self.log.error('Invalid guess %s: unknown word', self.guess)
            else:
                for i in range(5):
                    letter = self.guess.word[i]
                    if self.word[i] == letter:
                        self.log.info('%s is correct!', letter)
                    elif letter in self.word:
                        self.log.info('%s is close', letter)
                    else:
                        self.log.info('%s is wrong', letter)


    def addLetter(self, letter: str):
        self.guess.addLetter(letter.upper())
        self.log.info('Current guess: %s', self.guess)
        self.renderer.drawGuess(self.guess)
        if self.guess.isComplete():
            self.validateGuess()

    def onKeyUp(self, event):
        #self.log.info('Key pressed: %s', event.char)
        char = event.char
        if char >= 'a' and char <= 'z':
            #self.log.info('Valid letter: %s', char)
            self.addLetter(char)

    def createWidgets(self):
        """Create user widgets"""

        # Buttons
        self.btnStart  = self.addButton('Démarrer', self.newGame)

        # Canvas
        self.canGrid = tk.Canvas(master=self.frmMain, bg='#c0f0f0', bd=0, 
                                    height=self.iHeight, width=self.iWidth, highlightthickness=0)
        self.canGrid.pack(side=tk.LEFT)
        self.window.bind("<Key>", self.onKeyUp)
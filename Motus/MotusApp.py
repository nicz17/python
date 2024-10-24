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
from Renderer import *

class MotusApp(BaseApp):
    """Motus App window."""
    log = logging.getLogger('MotusApp')
    gridW = 5
    gridH = 6
    iSize = 100

    def __init__(self) -> None:
        """Constructor."""
        self.iHeight = self.gridH*self.iSize
        self.iWidth  = self.gridW*self.iSize
        sGeometry = '1000x800'
        super().__init__('Motus', sGeometry)
        self.getWords()
        self.guesses = []
        self.window.resizable(width=False, height=False)
        self.renderer = Renderer(self.gridW, self.gridH, self.canGrid, self.iSize, self.window)
        self.newGame()

    def newGame(self):
        """Start a new game with a random word."""
        self.log.info('New game started.')
        self.word = random.choice(self.words)
        #self.log.info('Secret word is %s', self.word)
        self.guesses = []
        self.newGuess()
        self.renderer.drawGrid()
        self.setStatus('Trouvez le mot de 5 lettres.')

    def newGuess(self):
        """Create a new word guess and append it to the list of guesses."""
        self.guess = Guess()
        self.guesses.append(self.guess)

    def gameOver(self, won: bool):
        """Game is over, won or lost."""
        msg = f'Bravo !\nTrouvé en {len(self.guesses)} essais.'
        if won:
            self.log.info('Found correct word %s in %d tries.', self.word, len(self.guesses))
        else:
            self.log.info('Failed to find correct word %s', self.word)
            msg = f'Echec !\nLe mot était {self.word}.'
        messagebox.showinfo(title='Motus', message=msg)
        self.newGame()

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
        """Validate the current complete guess."""
        self.log.info('Validating guess %s', self.guess)
        if self.guess.isComplete():
            isValid = True
            if not self.guess.word() in self.words:
                isValid = False
                self.log.error('Invalid guess %s: unknown word', self.guess.word())
                for letter in self.guess.letters:
                    letter.status = LetterStatus.Invalid
            else:
                for i in range(5):
                    letter = self.guess.letters[i]
                    if self.word[i] == letter.char:
                        self.log.info('%s is correct!', letter.char)
                        letter.status = LetterStatus.Correct
                    elif letter.char in self.word:
                        self.log.info('%s is close', letter.char)
                        letter.status = LetterStatus.Close
                    else:
                        self.log.info('%s is wrong', letter.char)
                        letter.status = LetterStatus.Wrong
            self.renderer.drawGuesses(self.guesses, isValid)

            if isValid:
                if self.word == self.guess.word():
                    # Success: word found
                    self.gameOver(True)
                elif len(self.guesses) < self.gridH:
                    # Not found yet, try again
                    self.newGuess()
                else:
                    # Failed: not found, no more guesses
                    self.gameOver(False)
            else:
                # Unknown word
                msg = f'Le mot {self.guess.word()} n\'est pas connu du jeu!'
                messagebox.showerror(title='Motus', message=msg)
        else:
            self.log.error('Trying to validate incomplete guess %s', self.guess)


    def addLetter(self, letter: str):
        """Add the specified letter to the current guess."""
        self.guess.addLetter(letter.upper())
        self.log.info('Current guess: %s', self.guess)
        self.renderer.drawGuesses(self.guesses)
        if self.guess.isComplete():
            self.validateGuess()

    def onKeyUp(self, event):
        """Keyboard char key pressed."""
        #self.log.info('Key pressed: %s', event.char)
        char = event.char
        if char >= 'a' and char <= 'z':
            #self.log.info('Valid letter: %s', char)
            self.addLetter(char)

    def onKeyDelete(self, event):
        """Keyboard delete key pressed."""
        self.log.info('Key pressed: Delete')
        self.guess.delete()
        self.renderer.drawGuesses(self.guesses)

    def createWidgets(self):
        """Create user widgets"""

        # Buttons
        #self.btnStart  = self.addButton('Démarrer', self.newGame)

        # Canvas
        self.canGrid = tk.Canvas(master=self.frmMain, bg='#c0f0f0', bd=0, 
                                    height=self.iHeight, width=self.iWidth, highlightthickness=0)
        self.canGrid.pack(side=tk.LEFT)

        # Keyboard bindings
        self.window.bind("<Key>", self.onKeyUp)
        self.window.bind("<BackSpace>", self.onKeyDelete)
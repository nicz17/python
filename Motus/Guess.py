"""
A word guess for the Motus game.
A guess is a 5 letter word.
Each letter may be correct, close, or wrong.
"""

from enum import Enum
import logging

class LetterStatus(Enum):
    """Enum of status for guess letters."""
    Pending  = 0
    Wrong    = 1
    Close    = 2
    Correct  = 3
    Invalid  = 4

    def __str__(self):
        return self.name
    
class Letter:
    def __init__(self, char: str) -> None:
        self.char = char
        self.status = LetterStatus.Pending
    
class Guess:
    log = logging.getLogger("Guess")

    def __init__(self) -> None:
        """No-arg constructor."""
        self.letters = []

    def addLetter(self, letter: str):
        """Adds a letter to this guess."""
        if not self.isComplete():
            self.letters.append(Letter(letter))
        return self

    def delete(self):
        """Deletes the last letter from this guess."""
        if len(self.letters) > 0:
            self.letters.pop()
            for letter in self.letters:
                letter.status = LetterStatus.Pending

    def isComplete(self):
        """Checks if all letters are defined."""
        return self.size() == 5
    
    def size(self):
        """Returns the letter count."""
        return len(self.letters)
    
    def word(self) -> str:
        """Combines the letters to form a word."""
        return ''.join(letter.char for letter in self.letters)
    
    def __iter__(self):
        """Iterates on our letters."""
        for letter in self.letters:
            yield letter
    
    def __str__(self):
        return f'Guess {self.word()}'
    

def testGuess():
    """Simple unit test"""
    guess = Guess()
    guess.addLetter('B').addLetter('R').addLetter('A').addLetter('V').addLetter('O')
    guess.log.info('%s is complete: %s', guess, guess.isComplete())
    guess.log.info(guess.word())

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s",
        level=logging.INFO, handlers=[logging.StreamHandler()])
    testGuess()
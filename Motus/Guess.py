"""
A word guess for the Motus game.
A guess is a 5 letter word.
Each letter may be correct, close, or wrong.
"""

from enum import Enum

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
    def __init__(self) -> None:
        self.letters = []

    def addLetter(self, letter: str):
        """Adds a letter to this guess."""
        if not self.isComplete():
            self.letters.append(Letter(letter))

    def delete(self):
        """Deletes the last letter from this guess."""
        if len(self.letters) > 0:
            self.letters.pop()
            for letter in self.letters:
                letter.status = LetterStatus.Pending

    def isComplete(self):
        """Cecks if all letters are defined."""
        return self.size() == 5
    
    def size(self):
        return len(self.letters)
    
    def word(self) -> str:
        word = ''
        for letter in self.letters:
            word += letter.char
        return word
    
    def __iter__(self):
        for letter in self.letters:
            yield letter
    
    def __str__(self):
        return self.word()
"""
A game with player info, score etc.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
import time

class Game:
    """Game with player name and score"""
    log = logging.getLogger(__name__)

    def __init__(self, sName: str, sPlayer: str, iScore: int, tStart = None, iProgress = 0):
        self.sName = sName
        self.sPlayer = sPlayer
        self.iScore = iScore
        self.iProgress = iProgress
        if tStart is None:
            self.tStart = time.time()
        else:
            self.tStart = tStart

    def incScore(self, iPoints: int):
        """Increment the score by the specified points."""
        self.iScore += iPoints

    def incProgress(self):
        """Increment the progress (finished objectives) by 1."""
        self.iProgress += 1

    def toJson(self):
        """Create a dict of this game for json export."""
        data = {}
        data['name']     = self.sName
        data['player']   = self.sPlayer
        data['score']    = self.iScore
        data['progress'] = self.iProgress
        data['start']    = self.tStart
        return data
    
    @staticmethod
    def fromJson(data):
        """Create a Game from the specified dict."""
        sName     = data.get('name', 'Qombo')
        sPlayer   = data.get('player', 'Guest')
        iScore    = data.get('score', 0)
        iProgress = data.get('progress', 0)
        tStart    = data.get('start', time.time())
        return Game(sName, sPlayer, iScore, tStart, iProgress)

    def __str__(self):
        return 'Game of ' + self.sName + ' for ' + self.sPlayer + ' score ' + str(self.iScore)
    


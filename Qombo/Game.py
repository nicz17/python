"""
A game with player info, score etc.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
import time

class Game:
    log = logging.getLogger(__name__)

    def __init__(self, sName: str, sPlayer: str, iScore: int, tStart = None):
        self.sName = sName
        self.sPlayer = sPlayer
        self.iScore = iScore
        if tStart is None:
            self.tStart = time.time()
        else:
            self.tStart = tStart

    def toJson(self):
        """Create a dict of this game for json export."""
        data = {}
        data['name']   = self.sName
        data['player'] = self.sPlayer
        data['score']  = self.iScore
        data['start']  = self.tStart
        return data

    def __str__(self):
        return 'Game of ' + self.sName + ' for ' + self.sPlayer + ' score ' + str(self.iScore)
    


"""
Save and load game state to and from JSON files. 
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import json
import logging
import os
import time
from Game import *
from Grid import *
from Qombit import *
from QombitFactory import *

class GameSave():
    """Save and load game state to and from JSON files."""
    log = logging.getLogger(__name__)
    dir = 'saves/'

    def __init__(self) -> None:
        self.log.info('GameSave to/from json in %s', self.dir)
        self.qombitFactory = QombitFactory()
        
        # Add save dir if missing
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def save(self, filename: str, game: Game, grid: Grid):
        """Saves the game state to a JSON file."""
        self.log.info('Saving game to %s%s', self.dir, filename)

        dData = {}
        dData['version'] = __version__
        dData['date']    = time.time()
        dData['game']    = game.toJson()
        dData['grid']    = grid.toJson()

        sJson = json.dumps(dData, indent=2)
        oFile = open(self.dir + filename, 'w')
        oFile.write(sJson)
        oFile.close()

    def load(self, filename: str, grid: Grid) -> Game:
        """Loads a game state from a JSON file."""
        self.log.info('Loading game from %s%s', self.dir, filename)
        if not os.path.exists(self.dir + filename):
            self.log.error('No such file: %s', self.dir + filename)
            return
        
        oFile = open(self.dir + filename, 'r')
        dData = json.load(oFile)
        dGrid = dData['grid']
        for dCell in dGrid['cells']:
            x = dCell['x']
            y = dCell['y']
            qombit = QombitFactory.fromJson(dCell['value'])
            self.log.info('Adding %s at [%d:%d]', str(qombit), x, y)
            grid.put(x, y, qombit)

        dGame = dData['game']
        game = Game(dGame['name'], dGame['player'], dGame['score'], dGame['start'])

        oFile.close()
        return game

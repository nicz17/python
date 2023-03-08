"""
Save and load game state to and from JSOn files. 
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import getpass
import json
import logging
import os
import time
from Grid import *

class GameSave():
    log = logging.getLogger(__name__)
    dir = 'saves/'

    def __init__(self) -> None:
        self.log.info('GameSave to/from json in %s', self.dir)
        
        # Add save dir if missing
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def save(self, filename: str, grid: Grid):
        self.log.info('Saving game to %s%s', self.dir, filename)

        dData = {}
        dData['game']    = 'Qombo'
        dData['version'] = __version__
        dData['player']  = getpass.getuser()
        dData['date']    = time.time()
        dData['grid']    = grid.toJson()

        sJson = json.dumps(dData, indent=2)
        oFile = open(self.dir + filename, 'w')
        oFile.write(sJson)
        oFile.close()

    def load(self, filename: str):
        self.log.info('Loading game from %s%s', self.dir, filename)
        self.log.error('Not implemented yet!')

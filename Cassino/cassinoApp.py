#!/usr/bin/env python3

"""
 The Cassino card game
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
from BaseApp import *
from playmat import Playmat

class CassinoApp(BaseApp):
    """Qombo App window."""
    log = logging.getLogger('CassinoApp')

    def __init__(self) -> None:
        self.iWidth  = 1500
        self.iHeight = 900
        self.dragdroptag = None
        self.playmat = Playmat(self.iWidth, self.iHeight)
        sGeometry = str(self.iWidth + 320) + 'x' + str(self.iHeight + 30)
        super().__init__('Cassino', sGeometry)
        self.window.resizable(width=False, height=False)
    
    def onSetPlayers(self):
        pass

    def onNewGame(self):
        pass

    def createWidgets(self):
        """Create user widgets."""

        # Buttons
        self.btnPlayers = self.addButton('Joueurs', self.onSetPlayers)
        self.btnStart   = self.addButton('Nouvelle partie', self.onNewGame)

        # Playmat
        self.playmat.createWidgets(self.frmMain)
        self.playmat.render()

def configureLogging():
    """Configures logging to have timestamped logs at INFO level."""
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
        level=logging.INFO,
        datefmt = '%Y.%m.%d %H:%M:%S',
        handlers=[logging.StreamHandler()])
    return logging.getLogger('Cassino')

def main():
    """Main routine."""
    log.info('Welcome to Cassino v' + __version__)
    app = CassinoApp()
    app.run()
    
log = configureLogging()
main()

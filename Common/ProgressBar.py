"""
 A progress bar with a number of steps
 and a color gradient.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
from Palette import *

class ProgressBar:
    log = logging.getLogger(__name__)

    def __init__(self, iTotal: int, oPalette = GreenRedPalette()) -> None:
        self.log.info('ProgressBar with %d steps', iTotal)
        self.oPalette = oPalette
        self.iTotal = iTotal
        self.iAt = 0

    def inc(self):
        self.iAt += 1

    def setAt(self, iAt: int):
        self.iAt = iAt

    def getColor(self) -> str:
        rFraction = float(self.iAt)/float(self.iTotal)
        return self.oPalette.getColorHex(rFraction)
    
    def getTextSteps(self) -> str:
        return f'{self.iAt} of {self.iTotal}'
    
    def getTextPercent(self) -> str:
        rPercent = 100.0*float(self.iAt)/float(self.iTotal)
        return f'{rPercent:.1f}%'


def testProgressBar():
    """UnitTest case"""
    oProgress = ProgressBar(25)
    oProgress.setAt(12)
    oProgress.log.info('Progress is %s', oProgress.getTextSteps())
    oProgress.log.info('Progress is %s', oProgress.getTextPercent())
    oProgress.log.info('Color is %s', oProgress.getColor())

if __name__ == '__main__':
    logging.basicConfig(format="[%(levelname)s] %(message)s", 
        level=logging.DEBUG, handlers=[logging.StreamHandler()])
    testProgressBar()

    
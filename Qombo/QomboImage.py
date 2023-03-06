"""
 An image representation of a Qombit.
 Image evolves with the Qombit level.
 It is colored using a Palette depending on the Qombit rarity.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

from PIL import Image
import numpy as np
import math
import logging
from Palette import *
from scipy.ndimage import gaussian_filter

class QomboImage:
    log = logging.getLogger('QomboImage')

    def __init__(self, sName: str, w: int, h: int):
        self.sName = sName
        self.w = w
        self.h = h
        self.iLevel = 1
        self.aMask = np.zeros((w, h))

    def generate(self, iLevel: int):
        """Generate the density mask."""
        self.iLevel = iLevel
        self.log.info('Generating %s', str(self))
        self.aMask = np.zeros((self.w, self.h))
        self.computeMask()
        self.normalize()

    def normalize(self):
        """Normalizes the density mask so that all values are between 0 and 1."""
        rMin = np.amin(self.aMask)
        self.aMask = self.aMask - rMin
        rMax = max(1.0, np.amax(self.aMask))
        self.aMask = self.aMask / rMax

    def computeMask(self):
        """Compute the image mask. Implemented by subclasses."""
        pass

    def toImage(self, oPalette: Palette, sFilename: str):
        self.log.info('Saving %s as %s with palette %s', str(self), sFilename, oPalette.sName)
        rgbArray = np.zeros((self.h, self.w, 3), 'uint8')
        for x in range(self.w):
            for y in range(self.h):
                col = oPalette.getColor(self.aMask[x][y])
                rgbArray[y, x, :] = col
        img = Image.fromarray(rgbArray)
        img.save(sFilename, 'PNG')

    def __str__(self) -> str:
        return self.sName + ' lvl' + str(self.iLevel) + ' ' + str(self.w) + 'x' + str(self.h)


class DiceImageMask(QomboImage):
    """A QomboImage imitating dice faces, but 1 to 9."""

    def __init__(self, w, h):
        super().__init__('DiceQomboImage', w, h)
    
    def computeMask(self):
        self.aMask = np.zeros((self.w, self.h))
        if self.iLevel %2 == 1:
            self.addDot(0.50, 0.50)
        if self.iLevel >= 2:
            self.addDot(0.22, 0.22)
            self.addDot(0.78, 0.78)
        if self.iLevel >= 4:
            self.addDot(0.78, 0.22)
            self.addDot(0.22, 0.78)
        if self.iLevel >= 6:
            self.addDot(0.22, 0.50)
            self.addDot(0.78, 0.50)
        if self.iLevel >= 8:
            self.addDot(0.50, 0.22)
            self.addDot(0.50, 0.78)
        self.aMask = gaussian_filter(self.aMask, self.w/16)

    def addDot(self, x, y):
        self.aMask[int(x*self.w), int(y*self.h)] = 10000.0
    

def testQomboImage():
    """Unit Test case."""
    nLevels = 10
    mask = DiceImageMask(100, 100)
    for iLevel in range(nLevels):
        mask.generate(iLevel)
        mask.toImage(PinkGreenPalette(), 'images/test0' + str(iLevel) + '.png')

if __name__ == '__main__':
    logging.basicConfig(format="[%(levelname)s] %(message)s", 
        level=logging.DEBUG, handlers=[logging.StreamHandler()])
    testQomboImage()
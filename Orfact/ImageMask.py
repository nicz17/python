"""
 An image as an array of doubles between 0 and 1.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

from PIL import Image
import numpy as np

class ImageMask:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def toImage(self, oPalette, sFilename):
        print('Saving', self.__str__(), 'as', sFilename, 'with palette', oPalette.sName)
        aMask = np.random.rand(self.w, self.h)
        rgbArray = np.zeros((self.h, self.w, 3), 'uint8')
        for x in range(self.w):
            for y in range(self.h):
                col = oPalette.getColor(aMask[x][y])
                rgbArray[y, x, :] = col
        img = Image.fromarray(rgbArray)
        img.save(sFilename, 'PNG')

    def __str__(self) -> str:
        return 'ImageMask ' + str(self.w) + 'x' + str(self.h)


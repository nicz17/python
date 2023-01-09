""" Palette
 A palette rendered as a color gradient
 using gaussian distributions
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import random
import math

from PIL import Image
import numpy as np

class Palette:
    sigma = 0.35

    def __init__(self, sName):
        self.sName = sName

    def toColorScale(self, sFilename, iWidth, iHeight):
        print(self.sName, 'generating', iWidth, 'x', iHeight, 'color scale as', sFilename)
        rgbArray = np.zeros((iHeight, iWidth, 3), 'uint8')
        for x in range(iWidth):
            col = self.getColor(x/iWidth)
            for y in range(iHeight):
                rgbArray[y, x, :] = col
        img = Image.fromarray(rgbArray)
        img.save(sFilename, 'PNG')

    def getColor(self, x):
        return [Palette.gauss(x, 0.75, self.sigma), Palette.gauss(x, 0.5, self.sigma), Palette.gauss(x, 0.25, self.sigma)]
    
    def gauss(x, mu, sig):
        return (int)(255. * math.exp(-(x-mu)*(x-mu)/(sig*sig)))

    def __str__(self):
        return self.sName
    def __repr__(self):
        return 'Palette ' + self.sName

class HeatPalette(Palette):
    sigma = 0.32

    def __init__(self):
        super().__init__("HeatPalette")

    def getColor(self, x):
        return [Palette.gauss(x, 0.72, self.sigma), Palette.gauss(x, 0.5, self.sigma), Palette.gauss(x, 0.28, self.sigma)]

class OraVioPalette(Palette):
    def __init__(self):
        super().__init__("OraVioPalette")

    def getColor(self, x):
        return [Palette.gauss(x, 1.035, 0.920), Palette.gauss(x, 0.619, 0.380), Palette.gauss(x, 0.370, 0.343)]

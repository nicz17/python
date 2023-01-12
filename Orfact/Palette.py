"""
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
#from NameGen import *

class Palette:
    sigma = 0.35

    def __init__(self, sName):
        self.sName = sName

    def toColorScale(self, sFilename, iWidth, iHeight):
        print('Saving', self.sName, iWidth, 'x', iHeight, 'color scale as', sFilename)
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

class RandomPalette(Palette):
    def __init__(self):
        #nameGen = NameGen(42)
        super().__init__('RandomPalette')
        self.sigma = self.random(0.1, 1.0)
        self.muR = random.random()
        self.muG = random.random()
        self.muB = random.random()
        print('RandomPalette params: ', self.getParams())

    def random(self, min, max):
        return min + (max - min)*random.random()

    def getParams(self):
        sParams  = 'sig=%.3f' % self.sigma
        sParams += ' R=%.3f' % self.muR
        sParams += ' G=%.3f' % self.muG
        sParams += ' B=%.3f' % self.muB
        return sParams

    def getColor(self, x):
        return [Palette.gauss(x, self.muR, self.sigma), Palette.gauss(x, self.muG, self.sigma), Palette.gauss(x, self.muB, self.sigma)]

class HeatPalette(Palette):
    sigma = 0.32

    def __init__(self):
        super().__init__("HeatPalette")

    def getColor(self, x):
        return [Palette.gauss(x, 0.72, self.sigma), Palette.gauss(x, 0.5, self.sigma), Palette.gauss(x, 0.28, self.sigma)]

class LinesPalette(Palette):
    sigma = 0.02

    def __init__(self):
        super().__init__("LinesPalette")

    def getColor(self, x):
        return [Palette.gauss(x, 0.9, self.sigma) + Palette.gauss(x, 0.7, self.sigma),
                Palette.gauss(x, 0.7, self.sigma) + Palette.gauss(x, 0.5, self.sigma) + Palette.gauss(x, 0.3, self.sigma), 
                Palette.gauss(x, 0.3, self.sigma) + Palette.gauss(x, 0.1, self.sigma)]

class CombPalette(Palette):
    width = 0.005

    def __init__(self):
        super().__init__("CombPalette")

    def getColor(self, x):
        return [self.dirac(x, 0.9) + self.dirac(x, 0.7),
                self.dirac(x, 0.7) + self.dirac(x, 0.5) + self.dirac(x, 0.3),
                self.dirac(x, 0.3) + self.dirac(x, 0.1)]
    
    def dirac(self, x, mu):
        if (abs(x - mu) <= self.width):
            return 255
        if (abs(x - mu) <= 2.0*self.width):
            return 128
        return 0

class OraVioPalette(Palette):
    def __init__(self):
        super().__init__("OraVioPalette")

    def getColor(self, x):
        return [Palette.gauss(x, 1.035, 0.920), Palette.gauss(x, 0.619, 0.380), Palette.gauss(x, 0.370, 0.343)]

class BlackHolePalette(Palette):
    def __init__(self):
        super().__init__("BlackHolePalette")

    def getColor(self, x):
        return [Palette.gauss(x, 0.4, 0.1), Palette.gauss(x, 0.4, 0.1), Palette.gauss(x, 0.2, 0.25)]

class GhostPalette(Palette):
    sigma = 0.42
    def __init__(self):
        super().__init__("GhostPalette")
    def getColor(self, x):
        return [Palette.gauss(x, 0.78, self.sigma), Palette.gauss(x, 0.81, self.sigma), Palette.gauss(x, 0.72, self.sigma)]

# Qydobu: sig=0.686 R=0.962 G=0.749 B=0.021
class BlueGoldPalette(Palette):
    sigma = 0.686
    def __init__(self):
        super().__init__("BlueGoldPalette")
    def getColor(self, x):
        return [Palette.gauss(x, 0.962, self.sigma), Palette.gauss(x, 0.749, self.sigma), Palette.gauss(x, 0.021, self.sigma)]

class GrayScalePalette(Palette):
    def __init__(self):
        super().__init__("GrayScale")

    def getColor(self, x):
        return (int)(255. * x)

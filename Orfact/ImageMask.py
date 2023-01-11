"""
 An image as an array of doubles between 0 and 1.
 Image can be saved as a grayscale
 or colored using a Palette.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

from PIL import Image
import numpy as np
import math

class ImageMask:
    def __init__(self, sName, w, h):
        self.sName = sName
        self.w = w
        self.h = h
        self.aMask = np.zeros((w, h))

    def generate(self):
        print('Generating', self.__str__())

    def toImage(self, oPalette, sFilename):
        print('Saving', self.__str__(), 'as', sFilename, 'with palette', oPalette.sName)
        rgbArray = np.zeros((self.h, self.w, 3), 'uint8')
        for x in range(self.w):
            for y in range(self.h):
                col = oPalette.getColor(self.aMask[x][y])
                rgbArray[y, x, :] = col
        img = Image.fromarray(rgbArray)
        img.save(sFilename, 'PNG')

    def toGrayScale(self, sFilename):
        print('Saving', self.__str__(), 'as', sFilename, 'grayscale')
        img = Image.fromarray(np.uint8(self.aMask * 255))
        img = img.rotate(270, expand=True)
        img.save(sFilename, 'PNG')

    def __str__(self) -> str:
        return self.sName + ' ' + str(self.w) + 'x' + str(self.h)

class RandomImageMask(ImageMask):
    def __init__(self, w, h):
        super().__init__('RandomImageMask', w, h)

    def generate(self):
        print('Generating', self.__str__())
        self.aMask = np.random.rand(self.w, self.h)

class LinearImageMask(ImageMask):
    def __init__(self, w, h):
        super().__init__('LinearImageMask', w, h)

    def generate(self):
        print('Generating', self.__str__())
        for x in range(self.w):
            for y in range(self.h):
                self.aMask[x, y] = (x + self.w * y)/(self.w * self.h)

class GaussImageMask(ImageMask):
    def __init__(self, w, h):
        super().__init__('GaussImageMask', w, h)

    def generate(self):
        print('Generating', self.__str__())
        for x in range(self.w):
            for y in range(self.h):
                dx = x - self.w/2
                dy = y - self.h/2
                dist = math.sqrt(dx*dx + dy*dy)
                self.aMask[x, y] = GaussImageMask.gauss(dist, 0.0, self.w/4.0)

    def gauss(x, mu, sig):
        return math.exp(-(x-mu)*(x-mu)/(sig*sig))

class ManhattanImageMask(ImageMask):
    def __init__(self, w, h):
        super().__init__('ManhattanImageMask', w, h)

    def generate(self):
        print('Generating', self.__str__())
        for x in range(self.w):
            for y in range(self.h):
                dx = abs(x - self.w/2)
                dy = abs(y - self.h/2)
                dist = dx + dy
                self.aMask[x, y] = ManhattanImageMask.gauss(dist, 0.0, self.w/4.0)

    def gauss(x, mu, sig):
        return math.exp(-(x-mu)*(x-mu)/(sig*sig))

class WaveImageMask(ImageMask):
    def __init__(self, freq, w, h):
        super().__init__('WaveImageMask', w, h)
        self.freq = freq

    def generate(self):
        print('Generating', self.__str__())
        for x in range(self.w):
            for y in range(self.h):
                self.aMask[x, y] = 0.25*(2.0 + math.sin(self.freq*x) + math.cos(self.freq*y))
                #self.aMask[x, y] = 0.5*(1.0 + math.sin(self.freq*(x+y)))  # diagonals

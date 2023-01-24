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
import random
import logging

class ImageMask:
    log = logging.getLogger('ImageMask')

    def __init__(self, sName, w, h):
        self.sName = sName
        self.w = w
        self.h = h
        self.aMask = np.zeros((w, h))

    def generate(self):
        """Generate the density mask."""
        self.log.info('Generating %s', self.__str__())

    def randomize(self):
        """Randomize the mask parameters."""
        self.log.info('Randomizing %s', self.__str__())

    def toImage(self, oPalette, sFilename):
        self.log.info('Saving %s as %s with palette %s', self.__str__(), sFilename, oPalette.sName)
        rgbArray = np.zeros((self.h, self.w, 3), 'uint8')
        for x in range(self.w):
            for y in range(self.h):
                col = oPalette.getColor(self.aMask[x][y])
                rgbArray[y, x, :] = col
        img = Image.fromarray(rgbArray)
        img.save(sFilename, 'PNG')

    def toGrayScale(self, sFilename):
        self.log.info('Saving %s as %s grayscale', self.__str__(), sFilename)
        img = Image.fromarray(np.uint8(self.aMask * 255))
        img = img.rotate(270, expand=True)
        img.save(sFilename, 'PNG')

    def gauss(x, mu, sig):
        return math.exp(-(x-mu)*(x-mu)/(sig*sig))

    def random(min, max):
        return min + (max - min)*random.random()

    def __str__(self) -> str:
        return self.sName + ' ' + str(self.w) + 'x' + str(self.h)

class RandomImageMask(ImageMask):
    def __init__(self, w, h):
        super().__init__('RandomImageMask', w, h)

    def generate(self):
        self.log.info('Generating %s', self.__str__())
        self.aMask = np.random.rand(self.w, self.h)

class LinearImageMask(ImageMask):
    def __init__(self, w, h):
        super().__init__('LinearImageMask', w, h)

    def generate(self):
        self.log.info('Generating %s', self.__str__())
        for x in range(self.w):
            for y in range(self.h):
                self.aMask[x, y] = (x + self.w * y)/(self.w * self.h)

class GaussImageMask(ImageMask):
    def __init__(self, w, h):
        super().__init__('GaussImageMask', w, h)

    def generate(self):
        self.log.info('Generating %s', self.__str__())
        for x in range(self.w):
            for y in range(self.h):
                dx = x - self.w/2
                dy = y - self.h/2
                dist = math.sqrt(dx*dx + dy*dy)
                self.aMask[x, y] = ImageMask.gauss(dist, 0.0, self.w/4.0)

class MultiGaussImageMask(ImageMask):
    def __init__(self, w, h):
        super().__init__('MultiGaussImageMask', w, h)

    def generate(self):
        nBlobs = random.randrange(6, 10)
        self.log.info('Generating %s with %d gaussians', self.__str__(), nBlobs)
        cx  = []
        cy  = []
        sig = []
        marginX = self.w/10
        marginY = self.h/10
        for i in range(nBlobs):
            cx.append(random.randrange(marginX, self.w - marginX))
            cy.append(random.randrange(marginY, self.h - marginY))
            sig.append(ImageMask.random(self.w/20, self.w/10))

        for x in range(self.w):
            for y in range(self.h):
                val = 0.0
                for i in range(nBlobs):
                    dx = x - cx[i]
                    dy = y - cy[i]
                    dist = math.sqrt(dx*dx + dy*dy)
                    val += ImageMask.gauss(dist, 0.0, sig[i])
                self.aMask[x, y] = min(1.0, val)

class ManhattanImageMask(ImageMask):
    def __init__(self, w, h):
        super().__init__('ManhattanImageMask', w, h)

    def generate(self):
        self.log.info('Generating %s', self.__str__())
        for x in range(self.w):
            for y in range(self.h):
                dx = abs(x - self.w/2)
                dy = abs(y - self.h/2)
                dist = dx + dy
                self.aMask[x, y] = ImageMask.gauss(dist, 0.0, self.w/4.0)

class WaveImageMask(ImageMask):
    def __init__(self, freq, w, h):
        super().__init__('WaveImageMask', w, h)
        self.freq = freq

    def generate(self):
        self.log.info('Generating %s', self.__str__())
        for x in range(self.w):
            for y in range(self.h):
                self.aMask[x, y] = 0.25*(2.0 + math.cos(self.freq*(x-self.w/2)) + math.cos(self.freq*(y-self.h/2)))
                #self.aMask[x, y] = 0.5*(1.0 + math.sin(self.freq*(x+y)))  # diagonals

class SineImageMask(ImageMask):
    def __init__(self, freq, w, h):
        super().__init__('SineImageMask', w, h)
        self.freq = freq
        self.fm = freq * (10.0 + 10.0*random.random())

    def generate(self):
        self.log.info('Generating %s', self.__str__())
        for x in range(self.w):
            for y in range(self.h):
                dx = 0.0
                dy = y - (self.h/2 + 20.0*math.sin(self.freq*x))
                dist = math.sqrt(dx*dx + dy*dy)
                self.aMask[x, y] = ImageMask.gauss(dist, 0.0, self.w/5.0)

# TODO SpiralImageMask
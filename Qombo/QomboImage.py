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
import logging
import os
from Palette import *
from HtmlPage import *
from scipy.ndimage import gaussian_filter

class QomboImage:
    log = logging.getLogger('QomboImage')

    def __init__(self, sName: str):
        self.sName = sName
        self.iLevel = 1
        self.aMask = None

    def generate(self, iLevel: int, w: int, h: int):
        """Generate the density mask."""
        self.iLevel = iLevel
        self.w = w
        self.h = h
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

    def gauss(x: float, mu: float, sig: float) -> float:
        """Gaussian distribution"""
        return math.exp(-(x-mu)*(x-mu)/(sig*sig))

    def getRho(self, x, y):
        """Get the normalized distance from image center."""
        dx = x - self.w/2
        dy = y - self.h/2
        return math.sqrt(dx*dx + dy*dy)/(float(self.h/2))

    def getPhi(self, x, y):
        """Get the angle from image center."""
        dx = x - self.w/2
        dy = y - self.h/2
        return math.atan2(-dx, dy)

    def __str__(self) -> str:
        return self.sName + ' lvl' + str(self.iLevel) + ' ' + str(self.w) + 'x' + str(self.h)


class DiceQomboImage(QomboImage):
    """A QomboImage imitating dice faces, but 1 to 9."""

    def __init__(self):
        super().__init__('DiceQomboImage')
    
    def computeMask(self):
        self.aMask = np.zeros((self.w, self.h))
        #self.aMask[0, 0] = -1000.0
        #self.aMask[0, self.h-1] = -1000.0
        #self.aMask[self.w-1, 0] = -1000.0
        #self.aMask[self.w-1, self.h-1] = -1000.0

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

class StarQomboImage(QomboImage):
    """A polar star image."""
    def __init__(self):
        super().__init__('StarQomboImage')

    def computeMask(self):
        for x in range(self.w):
            for y in range(self.h):
                rho = self.getRho(x, y)
                phi = self.getPhi(x, y) - 3.0*math.pi/4.0
                self.aMask[x, y] = math.sin(self.iLevel*phi) * QomboImage.gauss(rho, 0.5, 0.4)

class SpiralQomboImage(QomboImage):
    """A spiral image."""
    def __init__(self):
        super().__init__('SpiralQomboImage')

    def computeMask(self):
        for x in range(self.w):
            for y in range(self.h):
                rho = self.getRho(x, y)
                phi = self.getPhi(x, y)
                self.aMask[x, y] = math.sin(self.iLevel*phi + (self.iLevel+1)*rho) * QomboImage.gauss(rho, 0.5, 0.4)

class TargetQomboImage(QomboImage):
    """A target image."""
    def __init__(self):
        super().__init__('TargetQomboImage')

    def computeMask(self):
        for x in range(self.w):
            for y in range(self.h):
                rho = self.getRho(x, y)
                self.aMask[x, y] = math.sin(2*(self.iLevel+1)*rho)

class QuadrantQomboImage(QomboImage):
    """A quadrant image."""
    def __init__(self):
        super().__init__('QuadrantQomboImage')

    def computeMask(self):
        for x in range(self.w):
            for y in range(self.h):
                #rho = self.getRho(x, y)
                phi = self.getPhi(x, y) + math.pi
                if phi < self.iLevel*math.pi/4.0:
                    self.aMask[x, y] = phi

class RingQomboImage(QomboImage):
    """An image with 8 dots in a circle. The dot of our level is in a different color."""
    def __init__(self):
        super().__init__('RingQomboImage')

    def computeMask(self):
        self.aMask = np.zeros((self.w, self.h))
        for iOctant in range(8):
            x = int(0.5*self.w + 0.36*self.w*math.sin(iOctant*math.pi/4.0))
            y = int(0.5*self.h - 0.36*self.w*math.cos(iOctant*math.pi/4.0))
            self.aMask[x, y] = -10000
            if iOctant <= self.iLevel-1:
                self.aMask[x, y] = 10000
        self.aMask = gaussian_filter(self.aMask, self.w/16)

class JuliaQomboImage(QomboImage):
    """An image based on the Julia set fractal, with increasing precision."""

    def __init__(self):
        super().__init__('JuliaQomboImage')
        self.cParam = complex(-0.194, 0.6557)
        self.rWidth = 3.1
        self.iMaxIter = 200
        self.rBailout = 2.0

    def computeMask(self):
        self.iMaxIter = 10*self.iLevel
        for x in range(self.w):
            for y in range(self.h):
                self.aMask[x, y] = self.iter(self.getZ(x, y))

    def getZ(self, x, y):
        """Get the complex number corresponding to the image pixel x,y"""
        rw = self.rWidth
        rh = rw*self.h/self.w
        zr = x*rw/self.w - rw/2.0
        zi = y*rh/self.h - rh/2.0
        return complex(zr, zi)

    def iter(self, z):
        """Compute the iterations required to bailout at complex number z."""
        for i in range(self.iMaxIter):
            z = z*z + self.cParam
            if abs(z) > self.rBailout:
                return i
        return self.iMaxIter
    

def testQomboImage():
    """Unit Test case."""
    nLevels = 10
    dir = 'test/'
    aMasks = [DiceQomboImage(), StarQomboImage(), SpiralQomboImage(), RingQomboImage(), JuliaQomboImage()]
    oPalette = HeatPalette()
    #oPalette = NightPalette()
    #oPalette = FractalPalette()
        
    # Add save dir if missing
    if not os.path.exists(dir):
        os.makedirs(dir)

    aMaskImgs = []
    for oMask in aMasks:
        for iLevel in range(nLevels):
            sFilename = dir + oMask.sName + '0' + str(iLevel) + '.png'
            oMask.generate(iLevel, 160, 160)
            oMask.toImage(oPalette, sFilename)
            aMaskImgs.append(ImageHtmlTag(sFilename, oMask.sName + ' level ' + str(iLevel)))

    # Create HTML page for rendering
    oPage = HtmlPage('QomboImage Test')
    oPage.addHeading(1, 'QomboImage Test')
    oPage.addTable(aMaskImgs, nLevels)
    oPage.save('QomboImageTest.html')
    os.system('firefox QomboImageTest.html')

if __name__ == '__main__':
    logging.basicConfig(format="[%(levelname)s] %(message)s", 
        level=logging.DEBUG, handlers=[logging.StreamHandler()])
    testQomboImage()
"""
 Subclasses of SimulationMask based on polar coordinates.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import numpy as np
import math
import random
from scipy.ndimage.filters import gaussian_filter
from ImageMask import ImageMask
from SimulationMask import SimulationMask

class PolarImageMask(SimulationMask):
    """A SimulationMask based on polar coordinates."""

    def __init__(self, sName, w, h):
        super().__init__(sName, w, h)
        self.aMask = np.zeros((w, h))

    def getRho(self, x, y):
        """Get the normalized distance from image center."""
        dx = x - self.w/2
        dy = y - self.h/2
        return math.sqrt(dx*dx + dy*dy)/(float(self.h/2))

    def getPhi(self, x, y):
        """Get the angle from image center."""
        dx = x - self.w/2
        dy = y - self.h/2
        return math.atan2(dy, dx)

class RadarImageMask(PolarImageMask):
    """Simple polar image."""
    def __init__(self, w, h):
        super().__init__('RadarImageMask', w, h)

    def runSimulation(self):
        for x in range(self.w):
            for y in range(self.h):
                rho = self.getRho(x, y)
                phi = self.getPhi(x, y)
                self.aMask[x, y] = phi + 3.0*rho

class SpiralImageMask(PolarImageMask):
    """A spiral."""
    def __init__(self, w, h):
        super().__init__('SpiralImageMask', w, h)
        self.freq = 7.0
        self.curv = 13.0

    def randomize(self):
        super().randomize()
        self.freq = random.randrange(4, 16)
        self.curv = random.randrange(4, 16)

    def runSimulation(self):
        for x in range(self.w):
            for y in range(self.h):
                rho = self.getRho(x, y)
                phi = self.getPhi(x, y)
                self.aMask[x, y] = math.sin(self.freq*phi + self.curv*rho)

class StarFishImageMask(PolarImageMask):
    """A starfish-like image."""
    def __init__(self, w, h):
        super().__init__('StarFishImageMask', w, h)
        self.nBranches = 5
        self.mu = 0.5

    def randomize(self):
        super().randomize()
        self.nBranches = random.randrange(5, 9)
        self.mu = random.random()

    def runSimulation(self):
        for x in range(self.w):
            for y in range(self.h):
                rho = self.getRho(x, y)
                phi = self.getPhi(x, y)
                self.aMask[x, y] = math.sin(self.nBranches*phi) * ImageMask.gauss(rho, self.mu, 0.4)

class RoseWindowImageMask(PolarImageMask):
    """A rose-window style image."""
    def __init__(self, w, h):
        super().__init__('RoseWindowImageMask', w, h)
        self.nBranches = 5
        self.mu = 0.5

    def randomize(self):
        super().randomize()
        self.nBranches = random.randrange(4, 8)
        self.mu = random.random()/2.0

    def runSimulation(self):
        for x in range(self.w):
            for y in range(self.h):
                rho = self.getRho(x, y)
                phi = self.getPhi(x, y)
                v1 = math.sin(self.nBranches*phi) * ImageMask.gauss(rho, self.mu, 0.4)
                v2 = math.sin(-2.0*self.nBranches*phi) * ImageMask.gauss(rho, 0.4 + self.mu, 0.3)
                v3 = math.sin(4.0*self.nBranches*phi) * ImageMask.gauss(rho, 0.8 + self.mu, 0.25)
                v4 = math.sin(-8.0*self.nBranches*phi) * ImageMask.gauss(rho, 1.2 + self.mu, 0.2)
                self.aMask[x, y] = v1 + v2 + v3 + v4

"""
 Subclasses of ImageMask based on simulations.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import numpy as np
import math
import random
from scipy.ndimage.filters import gaussian_filter
from ImageMask import ImageMask

class SimulationMask(ImageMask):
    """An ImageMask based on a simulation."""

    def __init__(self, sName, w, h):
        super().__init__(sName, w, h)
        self.aMask = np.zeros((w, h))

    def generate(self):
        print('Generating', self.__str__())
        self.runSimulation()
        self.normalize()

    def runSimulation(self):
        """Runs the simulation to build the density mask."""
        pass

    def normalize(self):
        """Normalizes the density mask so that all values are between 0 and 1."""
        rMin = np.amin(self.aMask)
        self.aMask = self.aMask - rMin
        rMax = max(1.0, np.amax(self.aMask))
        self.aMask = self.aMask / rMax

class LorenzAttractorMask(SimulationMask):
    """An ImageMask based on the Lorenz Attractor.
       See https://itp.uni-frankfurt.de/~gros/Vorlesungen/SO/simulation_example/
    """
    def __init__(self, w, h, sName = 'LorenzAttractorMask'):
        super().__init__(sName, w, h)
        self.beta = 8.0/3.0
        self.sigma = 10.0
        self.rho = 27.0
        self.dt = 0.005

    def runSimulation(self):
        steps = 100000
        self.x = 1.0
        self.y = 1.0
        self.z = 0.5
        for step in range(steps):
            self.lorenz()
            self.aMask[int(6.0*self.x + self.w/2), int(self.h - 10 -5.0*self.z)] += self.y
            #print('step', step, 'x =', self.x, 'y =', self.y, 'z =', self.z)

    def lorenz(self):
        dx = self.sigma * (self.y - self.x)
        dy = self.x * (self.rho - self.z) - self.y
        dz = self.x * self.y - self.beta * self.z
        self.x += dx * self.dt
        self.y += dy * self.dt
        self.z += dz * self.dt

class RandomWalkMask(SimulationMask):
    """An ImageMask based on a random walk simulation."""

    def __init__(self, w, h, sName = 'RandomWalkMask'):
        super().__init__(sName, w, h)

    def runSimulation(self):
        steps = 8 * self.w * self.h
        self.randomWalk(steps)

    def randomWalk(self, steps):
        """A random walk starting at a random position and walking the specified number of steps"""
        self.x = random.randrange(0, self.w)
        self.y = random.randrange(0, self.h)

        for step in range(steps):
            dir = random.randint(1, 4)
            self.move(dir)
            self.aMask[self.x, self.y] += 1
            #self.aMask[self.x, self.y] = step
    
    def move(self, dir):
        """Moves the current position of the walk randomly left, right, up or down."""
        if (dir == 1):
            self.x += 1
        elif (dir == 2):
            self.x -= 1
        elif (dir == 3):
            self.y += 1
        elif (dir == 4):
            self.y -= 1
        
        if (self.x < 0): 
            self.x += self.w
        elif (self.x >= self.w):
            self.x -= self.w
        if (self.y < 0): 
            self.y += self.h
        elif (self.y >= self.h):
            self.y -= self.h

class MultiRandomWalkMask(RandomWalkMask):
    """An ImageMask based on multiple  random walks."""

    def __init__(self, w, h, sName = 'MultiRandomWalkMask'):
        super().__init__(w, h, sName)

    def runSimulation(self):
        walks = 5
        steps = 4000
        for walk in range(walks):
            self.randomWalk(steps)
            
class GaussianBlurMask(SimulationMask):
    """An ImageMask based on gaussian blurring of several dots."""

    def __init__(self, w, h):
        super().__init__('GaussianBlurMask', w, h)

    def runSimulation(self):
        self.aMask[int(self.w/2), int(self.h/2)] = 1000.0
        steps = 32
        for step in range(steps):
            x = random.randrange(10, self.w-10)
            y = random.randrange(10, self.h-10)
            self.aMask[x, y] = 200.0 + 800.0*random.random()

        self.aMask = gaussian_filter(self.aMask, sigma=6)

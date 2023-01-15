"""
 Subclasses of ImageMask based on simulations.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import numpy as np
import math
import random
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
        rMax = max(1.0, np.amax(self.aMask))
        self.aMask = self.aMask / rMax

class RandomWalkMask(SimulationMask):
    """An ImageMask based on a random walk simulation."""

    def __init__(self, w, h):
        super().__init__('RandomWalkMask', w, h)

    def runSimulation(self):
        steps = 8 * self.w * self.h
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
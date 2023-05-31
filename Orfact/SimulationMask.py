"""
 Subclasses of ImageMask based on simulations.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import numpy as np
import math
import random
from scipy.ndimage import gaussian_filter
from ImageMask import ImageMask
from Mesh import *

class SimulationMask(ImageMask):
    """An ImageMask based on a simulation."""

    def __init__(self, sName, w, h):
        super().__init__(sName, w, h)
        self.aMask = np.zeros((w, h))

    def generate(self):
        self.log.info('Generating %s', self.__str__())
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

    def drawLine(self, p1, p2, value: float):
        """Draw a line from p1 to p2."""
        nPoints = int(p1.dist(p2))
        #self.log.info('Drawing a line from %s to %s with %d points', p1, p2, nPoints)
        for i in range(nPoints):
            f = i / nPoints
            x = int(p1.x + f*(p2.x - p1.x))
            y = int(p1.y + f*(p2.y - p1.y))
            self.aMask[x, y] = value


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

class DiceImageMask(SimulationMask):
    """An ImageMask imitating dice faces."""

    def __init__(self, w, h):
        super().__init__('DiceImageMask', w, h)
        self.iValue = 5

    def randomize(self):
        self.iValue = random.randint(1, 9)
    
    def runSimulation(self):
        self.aMask = np.zeros((self.w, self.h))
        if self.iValue %2 == 1:
            self.addDot(0.50, 0.50)
        if self.iValue >= 2:
            self.addDot(0.22, 0.22)
            self.addDot(0.78, 0.78)
        if self.iValue >= 4:
            self.addDot(0.78, 0.22)
            self.addDot(0.22, 0.78)
        if self.iValue >= 6:
            self.addDot(0.22, 0.50)
            self.addDot(0.78, 0.50)
        if self.iValue >= 8:
            self.addDot(0.50, 0.22)
            self.addDot(0.50, 0.78)
        self.aMask = gaussian_filter(self.aMask, self.w/16)

    def addDot(self, x, y):
        self.aMask[int(x*self.w), int(y*self.h)] = 10000.0

    def __str__(self) -> str:
        return self.sName + ' ' + str(self.w) + 'x' + str(self.h) + ' ' + str(self.iValue)

class FractalMask(SimulationMask):
    """An ImageMask based on the Julia set fractal."""

    def __init__(self, w, h):
        super().__init__('FractalMask', w, h)
        self.cParam = complex(-0.73756, 0.16869)
        self.rWidth = 3.1
        self.iMaxIter = 200
        self.rBailout = 2.0

    def randomize(self):
        self.cParam = complex(-0.73756 + 0.002*random.random(), 0.16869 + 0.001*random.random())

    def runSimulation(self):
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
    
class MeshMask(SimulationMask):
    """A mask based on a random 2D triangle mesh."""

    def __init__(self, w, h):
        super().__init__('MeshMask', w, h)
        self.nVertices = 32

    def randomize(self):
        self.nVertices = 32

    def runSimulation(self):
        minDist = self.w/15.0
        mesh = Mesh()
        #for i in range(self.nVertices):
        while len(mesh.vertices) < self.nVertices:
            x = random.randrange(10, self.w-10)
            y = random.randrange(10, self.h-10)
            vertex = Vertex(x, y)
            closest = mesh.getClosest(vertex)
            if closest is not None:
                dist = vertex.dist(closest)
                if dist < minDist:
                    pass
                    #self.log.info('Discarding %s as it is only %f away from another vertex', vertex, dist)
                else:
                    mesh.addVertex(vertex)
            else:
                mesh.addVertex(vertex)

        mesh.buildEdges()
        self.log.info(mesh)

        for vertex in mesh.vertices:
            self.aMask[vertex.x, vertex.y] = 1000.0
        self.aMask = gaussian_filter(self.aMask, sigma=4)
        valEdges = 0.6*np.amax(self.aMask)
        for edge in mesh.edges:
            self.drawLine(edge.v1, edge.v2, valEdges)
        self.aMask = gaussian_filter(self.aMask, sigma=2)

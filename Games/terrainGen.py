#!/usr/bin/env python3
"""
Simple terrain generator using Perlin noise.
See https://pypi.org/project/pythonperlin/
See https://www.py4u.org/blog/python-random-map-generation-with-perlin-noise/
"""

import logging
import numpy as np
from pythonperlin import perlin
from PIL import Image
import pylab as plt
import random

class TerrainGenerator():
    """Height map generator using Perlin noise."""
    log = logging.getLogger('TerrainGenerator')

    def __init__(self):
        """Constructor with seed."""
        self.seed = random.randint(0, 42)
        self.grid = None

    def perlinNoise(self, size=512, gradients=8, octaves=3):
        """Generate Perlin noise."""
        shape = (gradients, gradients)
        self.log.info(f'Generating Perlin {shape} {size}px with {octaves} octaves')
        self.grid = perlin(shape, dens=int(size/gradients), seed=self.seed, octaves=octaves)

    def setElevation(self, min=-200, max=1200):
        """Set the terrain elevation to the specified range."""
        self.log.info(f'Setting elevation to [{min}:{max}]m')
        gmin = np.min(self.grid)
        gmax = np.max(self.grid)
        self.grid = ((self.grid-gmin)/(gmax-gmin))*(max-min) + min

    def plot(self):
        """Plot the generated terrain using pylab."""
        self.log.info('Plotting terrain map')
        plt.figure(figsize=(8,8))
        plt.imshow(self.grid, cmap=plt.get_cmap('Accent_r'))
        plt.axis('off')
        plt.show()

    def saveImage(self):
        """Save terrain as a grayscale image."""
        filename = 'images/terrain.png'
        image = Image.fromarray(self.grid.astype(np.uint8), mode='L')
        image.save(filename)
        self.log.info(f'Saved as {filename}')

# TODO class TerrainRenderer()


def configureLogging():
    """Configures logging to have timestamped logs at INFO level on stdout."""
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
        level=logging.INFO,
        datefmt='%Y.%m.%d %H:%M:%S',
        handlers=[logging.StreamHandler()])

def main():
    log.info('Welcome to terrainGen!')
    gen = TerrainGenerator()
    gen.perlinNoise(512, 4)
    gen.setElevation(0, 255)
    gen.saveImage()

configureLogging()
log = logging.getLogger('terrainGen')
main()
#!/usr/bin/env python3
"""
Simple terrain generator using Perlin noise.
Terrain rendering with colors.
See https://pypi.org/project/pythonperlin/
See https://www.py4u.org/blog/python-random-map-generation-with-perlin-noise/
"""

import logging
import os
import random

import numpy as np
import pylab as plt
from pythonperlin import perlin
from PIL import Image
from Palette import HeatPalette

class Terrain():
    """A generated terrain elevation map."""
    log = logging.getLogger('Terrain')

    def __init__(self, grid):
        self.grid = grid

    def __str__(self):
        return f'Terrain shape {self.grid.shape}'
    

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

    def getTerrain(self) -> Terrain:
        """Get the generated Terrain object."""
        return Terrain(self.grid)


class TerrainRenderer():
    """Class to render a terrain as an image."""
    log = logging.getLogger('TerrainRender')
    dir = 'images'

    def __init__(self):
        """Constructor."""
        self.palette = HeatPalette()
        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)

    def plot(self, terrain: Terrain):
        """Plot the terrain using pylab."""
        self.log.info('Plotting terrain map')
        plt.figure(figsize=(8,8))
        img = plt.imshow(terrain.grid, cmap=plt.get_cmap('terrain'))
        plt.colorbar(img, shrink=0.8)
        plt.axis('off')
        plt.title('Terrain height map')
        plt.show()

    def saveImageGrayscale(self, terrain: Terrain):
        """Save terrain as a grayscale image."""
        filename = f'{self.dir}/terrain.png'
        image = Image.fromarray(terrain.grid.astype(np.uint8), mode='L')
        image.save(filename)
        self.log.info(f'Saved as {filename}')

    def render(self, terrain: Terrain):
        """Render the terrain as a color image."""
        self.log.info(f'Rendering {terrain}')

        # Create RGB image array
        height = terrain.grid.shape[0]
        width  = terrain.grid.shape[1]
        color_grid = np.zeros((height, width, 3), dtype=np.uint8)
        
        for y in range(height):
            for x in range(width):
                elevation = terrain.grid[y][x]
                #color = self.getColor(elevation)
                color = self.getPaletteColor(elevation)
                color_grid[y][x] = color
        
        # Save colored image
        filename = f'{self.dir}/terrain.png'
        color_image = Image.fromarray(color_grid)
        color_image.save(filename)  
        self.log.info(f'Saved colored image as {filename}')  

    def getColor(self, elevation: float):  
        """Map elevation in meters to discrete terrain colors."""  
        if elevation < -50.0:       # Deep water
            return (0, 0, 100)      # Dark blue
        elif elevation < 0.0:       # Shallow water
            return (0, 100, 200)    # Light blue
        elif elevation < 50.0:      # Sand
            return (230, 200, 100)  # Tan
        elif elevation < 300.0:     # Grass
            return (34, 139, 34)    # Forest green
        elif elevation < 1000.0:    # Mountains
            return (139, 69, 19)    # Brown
        else:                       # Snow
            return (255, 255, 255)  # White

    def getPaletteColor(self, elevation: float):  
        """Map elevation in meters to continuous colors from a Palette."""
        # TODO try with pyplot colormaps terrain and ocean
        return self.palette.getColor(elevation/1000.0)


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
    gen.setElevation(-200, 1200)
    terrain = gen.getTerrain()
    ren = TerrainRenderer()
    ren.plot(terrain)
    ren.render(terrain)

configureLogging()
log = logging.getLogger('terrainGen')
main()
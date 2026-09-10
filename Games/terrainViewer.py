#!/usr/bin/env python3
"""Terrain viewer app."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.0"

import logging
import random
import tkinter as tk

from BaseApp import BaseApp
from NameGen import NameGen
from terrainGen import TerrainGenerator, TerrainRenderer
from Timer import Timer


class TerrainViewerApp(BaseApp):
    """Simple Terrain preview GUI."""
    log = logging.getLogger('TerrainViewerApp')

    def __init__(self, title, geometry='1000x650') -> None:
        self.size = 600
        super().__init__(title, geometry)
        self.terrain = None
        self.renderer = TerrainRenderer()
        self.renderer.buildColorCache()

    def generate(self):
        """Generates a terrain height map and displays a 2D preview."""
        self.setStatus('Création de terrain en cours ...')
        self.window.configure(cursor='watch')
        self.window.update()
        timer = Timer()

        # Use the same seed for all generators
        seed = random.randint(0, 42)

        # Give the terrain a random name
        nameGen = NameGen(seed)
        name = nameGen.generate()
        self.log.info(f'Generating terrain {name} size {self.size}')

        # Generate the height map
        gen = TerrainGenerator()
        gen.perlinNoise(self.size)
        gen.normalize()
        gen.shape()
        self.terrain = gen.getTerrain()

        # Render a 2D image of the terrain
        self.img = tk.PhotoImage(width=self.size, height=self.size)
        self.canTerrain.create_image(0, 0, anchor=tk.NW, image=self.img)
        for x in range(self.size):
            for y in range(self.size):
                #hexcolor = self.palette.getColorHex(self.terrain.grid[y][x])
                elevation = self.terrain.grid[y][x]
                hexcolor = self.renderer.getCachedColor(int(elevation*100.0))
                self.img.put(hexcolor, (x, y))

        # Save terrain image as PNG file
        filename = f'images/{name}{seed}.png'
        self.img.write(filename, 'PNG')
        self.log.info(f'Saved terrain images as {filename}')

        # Set done status
        runtime = timer.getElapsed()
        self.log.info(f'Generation done in {runtime}.')
        self.setStatus(f'Créé le terrain {name} en {runtime}')
        self.window.configure(cursor='')
    
    def onCanvasClick(self, event):
        """Zoom in on the point that was clicked."""
        self.log.info('Canvas clicked at %d:%d', event.x, event.y)
        self.lblCoords.configure(text=f'{event.x}:{event.y}')

    def onCanvasMove(self, event):
        self.lblCoords.configure(text=f'{event.x}:{event.y}')

    def onCanvasLeave(self, event):
        self.lblCoords.configure(text='')

    def createWidgets(self):
        """Create user widgets"""
        self.addButton('Générer', self.generate)

        self.lblCoords = tk.Label(master=self.frmBottom, text='Ready')
        self.lblCoords.pack(fill=tk.X, side=tk.RIGHT)

        self.canTerrain = tk.Canvas(master=self.frmMain, bg='#101010', bd=0, 
                                    height=self.size, width=self.size, highlightthickness=0)
        self.canTerrain.bind("<Button-1>", self.onCanvasClick)
        self.canTerrain.bind("<Motion>",   self.onCanvasMove)
        self.canTerrain.bind("<Leave>",    self.onCanvasLeave)
        self.canTerrain.pack(pady=6)
        

def configureLogging():
    """Configures logging to have timestamped logs at INFO level on stdout."""
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
        level=logging.INFO,
        datefmt='%Y.%m.%d %H:%M:%S',
        handlers=[logging.StreamHandler()])

def main():
    log.info('Welcome to terrainViewer!')
    app = TerrainViewerApp(f'Générateur de terrain v{__version__}')
    app.run()

configureLogging()
log = logging.getLogger('terrainViewer')
main()
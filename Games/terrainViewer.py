#!/usr/bin/env python3
"""Terrain viewer app."""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.0"

import logging
import random
import tkinter as tk
from tkinter import ttk

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
        nameGen = NameGen(seed, 3, 3, 0.01)
        name = nameGen.generate()
        self.log.info(f'Generating terrain {name} size {self.size}')
        self.lblName.configure(text=f'Ile {name}')

        # Generate the height map
        gen = TerrainGenerator(seed)
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
        """Handle canvas click event"""
        self.log.info('Canvas clicked at %d:%d', event.x, event.y)

    def onCanvasMove(self, event):
        """Handle canvas move event"""
        x = event.x
        y = event.y
        self.lblCoords.configure(text=f'{x}:{y}')
        if self.terrain:
            elevation = self.terrain.grid[y][x]*2000.0
            self.lblAltitude.configure(text=f'Altitude {elevation:.1f}m')

    def onCanvasLeave(self, event):
        """Handle canvas leave event"""
        self.lblCoords.configure(text='')
        self.lblAltitude.configure(text='')

    def createWidgets(self):
        """Create user widgets"""
        self.addButton('Générer', self.generate)

        self.frmLeft = ttk.Frame(master=self.frmMain, width=600)
        self.frmLeft.pack(fill=tk.Y, side=tk.LEFT)
        self.frmRight = ttk.Frame(master=self.frmMain, width=200)
        self.frmRight.pack(fill=tk.Y, side=tk.RIGHT, padx=6, pady=6)

        self.canTerrain = tk.Canvas(master=self.frmLeft, bg='#101010', bd=0, 
                                    height=self.size, width=self.size, highlightthickness=0)
        self.canTerrain.bind("<Button-1>", self.onCanvasClick)
        self.canTerrain.bind("<Motion>",   self.onCanvasMove)
        self.canTerrain.bind("<Leave>",    self.onCanvasLeave)
        self.canTerrain.pack(pady=6)

        self.lblName = tk.Label(master=self.frmRight, text='Sans nom')
        self.lblName.pack(fill=tk.X, side=tk.TOP)
        self.lblCoords = tk.Label(master=self.frmRight, text='')
        self.lblCoords.pack(fill=tk.X, side=tk.TOP)
        self.lblAltitude = tk.Label(master=self.frmRight, text='')
        self.lblAltitude.pack(fill=tk.X, side=tk.TOP)
        

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
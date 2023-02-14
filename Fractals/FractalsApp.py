"""
 Fractals App window based on BaseApp.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
import logging
from PIL import Image
import numpy as np
from BaseApp import *
from MandelbrotSet import *
from Palette import *
from Timer import *

class FractalsApp(BaseApp):
    log = logging.getLogger('FractalsApp')

    def __init__(self, sTitle, sGeometry = '1200x700') -> None:
        self.iSize = 600
        self.width = 3.0
        self.iMaxIter = 200
        self.oFractal = MandelbrotSet(self.iMaxIter, 2.0)
        self.oPalette = HeatPalette()
        self.center = complex(-0.75, 0.0)
        super().__init__(sTitle, sGeometry)

    def plot(self):
        self.setStatus('Plotting ' + self.oFractal.__str__())
        self.window.configure(cursor='watch')
        self.window.update()
        self.oPalette.toColorScale("images/palette.png", self.iSize, 50)
        self.oImgPal = tk.PhotoImage(file = "images/palette.png")
        self.canPalette.create_image(self.iSize - 50, 25, anchor=tk.CENTER, image=self.oImgPal)

        timer = Timer()
        dx = self.width/self.iSize
        bl = self.center - complex(self.width/2.0, self.width/2.0)
        rgbArray = np.zeros((self.iSize, self.iSize, 3), 'uint8')
        for x in range(self.iSize):
            for y in range(self.iSize):
                c = bl + complex(x*dx, y*dx)
                iter = self.oFractal.iter(c)
                color = self.oPalette.getColor(iter/self.iMaxIter)
                rgbArray[y, x, :] = color
                #self.image.putpixel((x, size-1-y), color)
            #if (x%16==0):
                #self.updateDisplay()
        #self.updateDisplay()

        img = Image.fromarray(rgbArray)
        img.save('images/fractal.png', 'PNG')
        self.oImgFract = tk.PhotoImage(file = "images/fractal.png")
        self.canFractal.create_image(0, 0, anchor=tk.NW, image=self.oImgFract)
        self.window.configure(cursor='')
        self.setStatus('Plotted ' + self.oFractal.__str__() + ' in ' + timer.getElapsed())
    

    def reset(self):
        self.setStatus('reset: Not implemented yet!')

    def createWidgets(self):
        """Create user widgets"""
        btnPlot = tk.Button(master=self.frmButtons, text='Plot', command=self.plot)
        btnPlot.pack(fill=tk.X)
        btnReset = tk.Button(master=self.frmButtons, text='Reset', command=self.reset)
        btnReset.pack(fill=tk.X)

        self.frmMain.configure(bg='black')
        self.canPalette = tk.Canvas(master=self.frmMain, bg='black', bd=0, 
                                    height=50, width=1100, highlightthickness=0)
        self.canPalette.pack()
        self.canFractal = tk.Canvas(master=self.frmMain, bg='red', bd=0, 
                                    height=self.iSize, width=self.iSize, highlightthickness=0)
        self.canFractal.pack()

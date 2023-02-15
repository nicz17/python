"""
 Fractals App window based on BaseApp.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
import logging
from BaseApp import *
from FractalSet import *
from Palette import *
from Timer import *

class FractalsApp(BaseApp):
    log = logging.getLogger('FractalsApp')

    def __init__(self, sTitle, sGeometry = '1200x700') -> None:
        self.iSize = 600
        self.iMaxIter = 200
        self.oFractal = MandelbrotSet(self.iMaxIter, 2.0)
        #self.oFractal = JuliaSet(self.iMaxIter, 2.0)
        #self.oFractal = BurningShip(self.iMaxIter, 2.0)
        #self.oPalette = HeatPalette()
        self.oPalette = DarkHeatPalette()
        self.center = self.oFractal.getDefaultCenter()
        self.width  = self.oFractal.getDefaultWidth()
        super().__init__(sTitle, sGeometry)

    def plot(self):
        self.setStatus('Plotting ' + self.oFractal.__str__())
        self.window.configure(cursor='watch')
        self.window.update()
        self.oPalette.toColorScale("images/palette.png", self.iSize, 50)
        self.oImgPal = tk.PhotoImage(file = "images/palette.png")
        self.canPalette.create_image(self.iSize - 50, 25, anchor=tk.CENTER, image=self.oImgPal)

        # Draw fractal on canvas live
        self.oImgFract = tk.PhotoImage(width=self.iSize, height=self.iSize)
        self.canFractal.create_image(0, 0, anchor=tk.NW, image=self.oImgFract)
        timer = Timer()
        dx = self.width/self.iSize
        bl = self.center - complex(self.width/2.0, self.width/2.0)
        for x in range(self.iSize):
            for y in range(self.iSize):
                c = bl + complex(x*dx, y*dx)
                iter = self.oFractal.iter(c)
                sColor = self.oPalette.getColorHex(iter/self.iMaxIter)
                self.oImgFract.put(sColor, (x, y))
            if (x % 20 == 0):
                self.window.update()

        self.window.configure(cursor='')
        self.setStatus('Plotted ' + self.oFractal.__str__() + ' in ' + timer.getElapsed())
    
    def onCanvasClick(self, event):
        self.log.info('Canvas clicked at %d:%d', event.x, event.y)
        bl = self.center - complex(self.width/2.0, self.width/2.0)
        at = bl + complex(event.x*self.width/self.iSize, event.y*self.width/self.iSize)
        self.log.info('Canvas clicked at %s', at.__str__())
        self.center = at
        self.width = 0.25*self.width
        self.plot()
        
    def reset(self):
        self.setStatus('Resetting ' + self.oFractal.__str__())
        self.center = self.oFractal.getDefaultCenter()
        self.width  = self.oFractal.getDefaultWidth()

    def setPalette(self):
        self.setStatus('Set palette: not implemented yet')

    def createWidgets(self):
        """Create user widgets"""
        btnPlot = tk.Button(master=self.frmButtons, text='Plot', command=self.plot)
        btnPlot.pack(fill=tk.X)
        btnReset = tk.Button(master=self.frmButtons, text='Reset', command=self.reset)
        btnReset.pack(fill=tk.X)
        self.addButton('Palette', self.setPalette)

        self.frmMain.configure(bg='black')
        self.canPalette = tk.Canvas(master=self.frmMain, bg='black', bd=0, 
                                    height=50, width=1100, highlightthickness=0)
        self.canPalette.pack()
        self.canFractal = tk.Canvas(master=self.frmMain, bg='#101010', bd=0, 
                                    height=self.iSize, width=self.iSize, highlightthickness=0)
        self.canFractal.bind("<Button-1>", self.onCanvasClick)
        self.canFractal.pack()

    def addButton(self, sText, fnCmd):
        btn = tk.Button(master=self.frmButtons, text=sText, command=fnCmd)
        btn.pack(fill=tk.X)

"""
 Fractals App window based on BaseApp.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
import logging
from BaseApp import *
from FractalSet import *
from Palette import *
from Timer import *

class FractalsApp(BaseApp):
    log = logging.getLogger('FractalsApp')

    def __init__(self, sTitle, sGeometry = '1000x650') -> None:
        self.iSize = 600
        self.iMaxIter = 200
        self.aFractals = [MandelbrotSet(self.iMaxIter), 
                          JuliaSet(self.iMaxIter), 
                          BurningShip(self.iMaxIter), 
                          LogisticMap(self.iMaxIter),
                          SineFractal(self.iMaxIter)]
        self.oFractal = self.aFractals[0]
        self.aPalettes = [FractalPalette(), FluoPalette(),
                          HeatPalette(), DarkHeatPalette(), 
                          SepiaPalette(), GhostPalette()]
        self.oPalette = self.aPalettes[0]
        self.center = self.oFractal.getDefaultCenter()
        self.width  = self.oFractal.getDefaultWidth()
        super().__init__(sTitle, sGeometry)
        self.plotPalette()

    def plot(self):
        """Compute the fractal and draw it live on the canvas."""
        self.setStatus('Plotting ' + self.oFractal.__str__())
        self.window.configure(cursor='watch')
        self.window.update()

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

    def plotPalette(self):
        """Draw palette color scale on canvas"""
        self.log.info('Plotting %s', self.oPalette.__str__())
        self.oImgPal = tk.PhotoImage(width=50, height=self.iSize)
        for x in range(50):
            for y in range(self.iSize):
                sColor = self.oPalette.getColorHex(y/self.iSize)
                self.oImgPal.put(sColor, (x, y))
        self.canPalette.create_image(0, 0, anchor=tk.NW, image=self.oImgPal)
        self.window.update()
    
    def onCanvasClick(self, event):
        """Zoom in on the point that was clicked."""
        self.log.info('Canvas clicked at %d:%d', event.x, event.y)
        bl = self.center - complex(self.width/2.0, self.width/2.0)
        at = bl + complex(event.x*self.width/self.iSize, event.y*self.width/self.iSize)
        self.log.info('Canvas clicked at %s', at.__str__())
        self.center = at
        self.width = 0.25*self.width
        self.plot()

    def onZoomOut(self):
        """Zoom back out."""
        self.width = 4.0*self.width
        self.plot()

    def onSaveImage(self):
        """Save the current image as PNG file."""
        sFilename = 'fractal.png'
        dicTypes = [('PNG images', '*.png')]
        oFile = asksaveasfile(initialfile = sFilename, 
                              filetypes = dicTypes, 
                              defaultextension = '*.png')
        if (oFile):
            sFilename = oFile.name
            self.setStatus('Saving image as ' + sFilename)
            oFile.close()
            self.oImgFract.write(sFilename, 'PNG')
        
    def reset(self):
        """Reset the current fractal to its default center and width."""
        self.setStatus('Resetting ' + self.oFractal.__str__())
        self.center = self.oFractal.getDefaultCenter()
        self.width  = self.oFractal.getDefaultWidth()
        self.plot()

    def createWidgets(self):
        """Create user widgets"""
        self.addButton('Plot', self.plot)
        self.addButton('Zoom out', self.onZoomOut)
        self.addButton('Reset', self.reset)
        self.addButton('Save image', self.onSaveImage)

        self.frmMain.configure(bg='black')
        self.canPalette = tk.Canvas(master=self.frmMain, bg='red', bd=0, 
                                    height=self.iSize, width=50, highlightthickness=0)
        self.canPalette.pack(side=tk.LEFT)
        self.canFractal = tk.Canvas(master=self.frmMain, bg='#101010', bd=0, 
                                    height=self.iSize, width=self.iSize, highlightthickness=0)
        self.canFractal.bind("<Button-1>", self.onCanvasClick)
        self.canFractal.pack()

        self.addFractalSelector()
        self.addPaletteSelector()

    def onFractalSelect(self, event):
        """Select the fractal that was chosen in the selector."""
        sName = self.varFractal.get()
        self.setStatus('Fractal selected: ' + sName)
        for oFractal in self.aFractals:
            if oFractal.sName == sName:
                self.oFractal = oFractal
                self.reset()
                break

    def onPaletteSelect(self, event):
        """Select the palette that was chosen in the selector."""
        sName = self.varPalette.get()
        self.setStatus('Palette selected: ' + sName)
        for oPalette in self.aPalettes:
            if oPalette.sName == sName:
                self.oPalette = oPalette
                self.plotPalette()
                break

    def addFractalSelector(self):
        """Add a Ttk ComboBox for selecting a fractal."""
        aNames = []
        for oFractal in self.aFractals:
            aNames.append(oFractal.sName)

        self.varFractal = tk.StringVar()
        cboFractal = ttk.Combobox(self.frmButtons, textvariable=self.varFractal, state = 'readonly')
        cboFractal['values'] = aNames
        cboFractal.current(0)
        cboFractal.bind('<<ComboboxSelected>>', self.onFractalSelect)
        cboFractal.pack(fill=tk.X, padx=4, pady=2)

    def addPaletteSelector(self):
        """Add a Ttk ComboBox for selecting a palette."""
        aNames = []
        for oPalette in self.aPalettes:
            aNames.append(oPalette.sName)

        self.varPalette = tk.StringVar()
        cboPalette = ttk.Combobox(self.frmButtons, textvariable=self.varPalette, state = 'readonly')
        cboPalette['values'] = aNames
        cboPalette.current(0)
        cboPalette.bind('<<ComboboxSelected>>', self.onPaletteSelect)
        cboPalette.pack(fill=tk.X, padx=4, pady=2)

    def addButton(self, sText, fnCmd):
        """Add a button with the specified label and callback."""
        btn = tk.Button(master=self.frmButtons, text=sText, command=fnCmd)
        btn.pack(fill=tk.X, padx=4, pady=2)

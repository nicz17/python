"""
 Demo for random Palette generation.
 Builds an Html page with various random palettes.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import os
import time

from Palette import *
from NameGen import *
from HtmlPage import *

class DemoPalette:
    def __init__(self) -> None:
        self.sTitle = 'Palette Demo'
        self.size = 300
        self.dir = 'palettes/'

    def run(self):
        print('Running', self.sTitle)
        tStart = time.time()
        
        # Add dir if missing
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        # Add reference palette
        aPalImgs = []
        oPal = HeatPalette()
        sFilename = self.dir + oPal.sName + '.png'
        oPal.toColorScale(sFilename, self.size, 20)
        aPalImgs.append(ImageHtmlTag(sFilename, oPal.sName))
        aPalImgs.append(HtmlTag('p', oPal.sName))

        # Add random palettes
        nPals = 12
        nameGen = NameGen(42)
        for i in range(nPals):
            sName = nameGen.generate()
            oPal = RandomPalette()
            sFilename = self.dir + oPal.sName + '-' + sName + '.png'
            oPal.toColorScale(sFilename, self.size, 20)
            aPalImgs.append(ImageHtmlTag(sFilename, sName))
            aPalImgs.append(HtmlTag('p', sName + ': ' + oPal.getParams()))

        # Create HTML page for rendering
        oPage = HtmlPage(self.sTitle, 'orfact.css')
        oPage.addHeading(1, self.sTitle)
        oPage.addTable(aPalImgs, 2)
        oPage.save('PaletteDemo.html')

        # Done
        tEnd = time.time()
        print(self.sTitle, 'done in %.3fs' % (tEnd-tStart))

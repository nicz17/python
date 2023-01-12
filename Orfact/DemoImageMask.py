"""
 Demo for ImageMask generation.
 Builds an Html page with variously rendered image masks.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import os
import time
from Palette import *
from ImageMask import *
from HtmlPage import *

class DemoImageMask:
    def __init__(self) -> None:
        self.sTitle = 'ImageMask Demo'
        self.size = 300
        self.dir = 'images/'

    def run(self):
        print('Running', self.sTitle)
        tStart = time.time()
        
        # Add dir if missing
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        # Define palettes and create their color scales
        aPals = [GrayScalePalette(), LinesPalette(), HeatPalette(), GhostPalette(), RandomPalette()]
        aPalImgs = []
        for oPal in aPals:
            sFilename = self.dir + oPal.sName + '.png'
            oPal.toColorScale(sFilename, self.size, 20)
            aPalImgs.append(ImageHtmlTag(sFilename, oPal.sName))

        # Define ImageMasks and render them with each palette
        aMasks = [GaussImageMask(self.size, self.size), 
                  ManhattanImageMask(self.size, self.size),
                  WaveImageMask(0.0628, self.size, self.size)]
        aMaskImgs = []
        for oMask in aMasks:
            oMask.generate()
            for oPal in aPals:
                sFilename = self.dir + oMask.sName + '-' + oPal.sName + '.png'
                oMask.toImage(oPal, sFilename)
                aMaskImgs.append(ImageHtmlTag(sFilename, oMask.sName + ' rendered with ' + oPal.sName))

        # Create HTML page for rendering
        oPage = HtmlPage(self.sTitle, 'orfact.css')
        oPage.addHeading(1, self.sTitle)

        oPage.addHeading(2, 'Palettes')
        oPage.addTable(aPalImgs, len(aPals))

        oPage.addHeading(2, 'Image masks')
        oPage.addTable(aMaskImgs, len(aPals))

        oPage.save('ImageMaskDemo.html')

        # Done
        tEnd = time.time()
        print(self.sTitle, 'done in %.3fs' % (tEnd-tStart))
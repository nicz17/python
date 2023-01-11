"""
 Demo for ImageMask generation.
 Builds an Html page with variously rendered image masks.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import sys

from Palette import *
from ImageMask import *
from HtmlPage import *

class DemoImageMask:
    def __init__(self) -> None:
        self.size = 300
        self.dir = 'images/'

    def run(self):
        print('Running ImageMask demo')

        # Define palettes and create their color scales
        aPals = [GrayScalePalette(), LinesPalette(), HeatPalette(), RandomPalette()]
        aPalImgs = []
        for oPal in aPals:
            sFilename = self.dir + oPal.sName + '.png'
            oPal.toColorScale(sFilename, self.size, 20)
            aPalImgs.append(ImageHtmlTag(sFilename, oPal.sName))

        # Define ImageMasks and render them with each palette
        aMasks = [GaussImageMask(self.size, self.size), ManhattanImageMask(self.size, self.size)]
        aMaskImgs = []
        for oMask in aMasks:
            oMask.generate()
            for oPal in aPals:
                sFilename = self.dir + oMask.sName + '-' + oPal.sName + '.png'
                oMask.toImage(oPal, sFilename)
                aMaskImgs.append(ImageHtmlTag(sFilename, oMask.sName + ' rendered with ' + oPal.sName))

        # Create HTML page for rendering
        oPage = HtmlPage('ImageMask Demo', 'orfact.css')
        oPage.addHeading(1, 'ImageMask Demo')

        oPage.addHeading(2, 'Palettes')
        oPage.addTable(aPalImgs)

        oPage.addHeading(2, 'Image masks')
        oPage.addTable(aMaskImgs, len(aPals))

        oPage.save('ImageMaskDemo.html')
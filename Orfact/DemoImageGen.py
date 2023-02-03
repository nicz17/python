"""
 Demo for random Image generation.
 Builds an Html page with variously rendered image masks.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import os
import logging
from Palette import *
from ImageMask import *
from SimulationMask import *
from PolarMask import *
from HtmlPage import *
from Timer import Timer

class DemoImageGen:
    log = logging.getLogger('DemoImageGen')

    def __init__(self) -> None:
        self.sTitle = 'ImageGen Demo'
        self.size = (600, 400)
        self.dir = 'images/'

    def run(self):
        self.log.info('Running %s', self.sTitle)
        timerDemo = Timer()
        
        # Add dir if missing
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        # Define ImageMasks to choose from
        aMasks = [#MultiGaussImageMask(self.size[0], self.size[1]),
                  #GaussianBlurMask(self.size[0], self.size[1]),
                  #RandomWalkMask(self.size[0], self.size[1]),
                  #SpiralImageMask(self.size[0], self.size[1]),
                  StarFishImageMask(self.size[0], self.size[1]),
                  RoseWindowImageMask(self.size[0], self.size[1])
                  ]
        nImages = 4
        aMaskImgs = []
        for i in range(nImages):
            oMask = random.choice(aMasks)
            oMask.randomize()
            oMask.generate()
            oPal = RandomPalette()
            sFilename = self.dir + 'RandomImage0' + str(i) + '.png'
            oMask.toImage(oPal, sFilename)
            aMaskImgs.append(ImageHtmlTag(sFilename, oMask.sName + ' rendered with ' + oPal.sName))

        # Create HTML page for rendering
        oPage = HtmlPage(self.sTitle, 'orfact.css')
        oPage.addHeading(1, self.sTitle)
        oPage.addTable(aMaskImgs, 2)

        oPage.save('ImageGenDemo.html')

        # Done
        timerDemo.stop()
        self.log.info('%s done in %s', self.sTitle, timerDemo.getElapsed())
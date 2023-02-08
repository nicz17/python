"""
 Multiple photo galleries.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import os
import sys
import logging
import glob
from Gallery import *
from HtmlPage import *

class MultiGallery:
    log = logging.getLogger('MultiGallery')
    
    def __init__(self, sPath):
        self.sPath = sPath
        self.aGals = []

    def build(self):
        aDirs = sorted(os.listdir(self.sPath))
        self.log.info('Building galleries from %d dirs', len(aDirs))
        for sDir in aDirs:
            self.log.info('Building gallery %s', sDir)
            gal = Gallery(self.sPath + sDir + '/')
            gal.build()
            if gal.size() > 0:
                self.aGals.append(gal)
        self.createIndex()
    
    def createIndex(self):
        sTitle = 'Galleries'
        aImgLinks = []
        for gal in self.aGals:
            sFile = gal.getSingleImage()
            sCaption = gal.getTitle() + ' - ' + str(gal.size()) + ' photos'
            tLink = LinkHtmlTag(gal.sPath + 'index.html', None)
            tLink.addTag(ImageHtmlTag(sFile, sCaption))
            tLink.addTag(GrayFontHtmlTag('<br>' + sCaption))
            aImgLinks.append(tLink)

        page = HtmlPage(sTitle, 'style.css')
        page.addHeading(1, sTitle)
        page.addTable(aImgLinks, 4, True).addAttr('width', '100%')
        page.add(LinkHtmlTag('links.html', 'Liens'))
        page.save(self.sPath + 'index.html')

        
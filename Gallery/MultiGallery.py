"""
 Multiple photo galleries.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import os
import logging
from Gallery import *
from TF79Gallery import *
from HtmlPage import *

class MultiGallery:
    log = logging.getLogger('MultiGallery')
    
    def __init__(self, sPath, bRecursive=False):
        self.sPath = sPath
        self.bRecursive = bRecursive
        self.aGals = []

    def build(self):
        if (self.bRecursive):
            self.log.info('Building recursive galleries from %s', self.sPath)
            return self.buildRecursive(self.sPath)
        
        aDirs = sorted(os.listdir(self.sPath))
        self.log.info('Building galleries from %d dirs', len(aDirs))
        for sDir in aDirs:
            self.log.info('Building gallery %s', sDir)
            gal = Gallery(self.sPath + sDir + '/')
            gal.build()
            if gal.size() > 0:
                self.aGals.append(gal)
        self.createIndex()

    def buildRecursive(self, sPath):
        aNodes = sorted(os.listdir(sPath))
        for sNode in aNodes:
            if os.path.isdir(sPath + sNode):
                sDir = sPath + sNode + '/'
                if self.hasPhotoDir(sDir):
                    self.log.info('%s has photos, will build index', sDir)
                    gal = TF79Gallery(sDir)
                    gal.build()
                else:
                    self.log.info('%s has no photos dir, recursing', sDir)
                    self.buildRecursive(sDir)
            #else:
                #self.log.info('%s is not a directory, skipping', sPath + sNode)

    def hasPhotoDir(self, sDir):
        return os.path.isdir(sDir + 'photos')
    
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

        
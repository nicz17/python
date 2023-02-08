"""
 A photo gallery.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import os
import sys
import logging
import glob
from HtmlPage import *

class Gallery:
    log = logging.getLogger('Gallery')
    
    def __init__(self, sPath):
        self.sPath = sPath
        self.aImgs = None
        
    def build(self):
        self.log.info('Building gallery at %s', self.sPath)
        self.aImgs = sorted(glob.glob(self.sPath + '*.jpg'))
        self.log.info('Found %d photos', len(self.aImgs))
        self.createThumbs()
        self.createIndex()

    def createThumbs(self):
        dirThumbs = self.sPath + 'thumbs/'

        if not os.path.exists(dirThumbs):
            os.makedirs(dirThumbs)

        for sImg in self.aImgs:
            sThumb = dirThumbs + os.path.basename(sImg)
            if not os.path.exists(sThumb):
                self.log.info('Creating thumbnail image %s', sThumb)
                sCmd = 'convert ' + sImg + ' -resize 180x180 ' + sThumb
                os.system(sCmd)

    def createIndex(self):
        dirThumbs = self.sPath + 'thumbs/'
        aImgLinks = []
        for sImg in self.aImgs:
            sFile = os.path.basename(sImg)
            sThumb = dirThumbs + sFile
            tLink = LinkHtmlTag(sFile, None)
            tLink.addTag(ImageHtmlTag(sThumb, sThumb))
            aImgLinks.append(tLink)

        page = HtmlPage('Gallery')
        page.addHeading(1, self.sPath)
        page.addTable(aImgLinks, 4, True).addAttr('width', '100%')
        page.save(self.sPath + 'index.html')

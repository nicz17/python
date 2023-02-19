"""
 A photo gallery.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import os
import re
import logging
import glob
from HtmlPage import *

class Gallery:
    log = logging.getLogger('Gallery')
    
    def __init__(self, sPath):
        self.sPath = sPath
        self.aImgs = None
        
    def build(self):
        self.aImgs = sorted(glob.glob(self.sPath + '*.jpg'))
        self.log.info('Building gallery at %s with %s photos', self.sPath, len(self.aImgs))
        if len(self.aImgs) > 0:
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
        sTitle = self.getTitle()
        dirThumbs = self.sPath + 'thumbs/'
        aImgLinks = []
        for sImg in self.aImgs:
            sFile = os.path.basename(sImg)
            sThumb = dirThumbs + sFile
            sCaption = self.getCaption(sFile)
            #self.log.info("Caption of %s is %s", sFile, sCaption)
            tLink = LinkHtmlTag(sFile, None)
            tLink.addTag(ImageHtmlTag(sThumb, sThumb))
            tLink.addTag(GrayFontHtmlTag('<br>' + sCaption))
            aImgLinks.append(tLink)

        page = HtmlPage('Gallery - ' + sTitle, self.getStyle())
        page.addHeading(1, sTitle)
        page.addTable(aImgLinks, self.getPicsPerRow(), True).addAttr('width', '100%')
        page.add(LinkHtmlTag('../index.html', 'Retour'))
        page.save(self.sPath + 'index.html')

    def getTitle(self):
        sTitle = os.path.basename(os.path.normpath(self.sPath)).capitalize()
        return sTitle

    def getCaption(self, sFile):
        """Return the caption for the specified photo."""
        sCaption = sFile.replace('.jpg', '')
        sCaption = re.sub(r'(\d+)$', r' \1', sCaption)
        sCaption = sCaption.replace('-', ' ')
        return sCaption.capitalize()
    
    def getStyle(self):
        """Get the CSS stylesheet path"""
        return '../style.css'
    
    def getPicsPerRow(self):
        """Number of pictures per row in index page"""
        return 4
    
    def getSingleImage(self):
        if len(self.aImgs) > 0:
            sImg = self.aImgs[0]
            sThumb = self.sPath + 'thumbs/' + os.path.basename(sImg)
            return sThumb
        return None
    
    def size(self):
        return len(self.aImgs)
    

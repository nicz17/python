"""
 A Gallery subclass to create the galleries on tf79.ch.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import os
import re
import logging
import glob
from HtmlPage import *
from GalleryHtmlPage import *
from Gallery import *

class TF79Gallery(Gallery):
    log = logging.getLogger('TF79Gallery')
    
    def __init__(self, sPath):
        self.sPath = sPath
        self.aImgs = None
        self.dicCaptions = None

    def build(self):
        self.aImgs = sorted(glob.glob(self.sPath + 'photos/*.jpg'))
        self.readCaptionsFile()
        self.log.info('Building TF79.ch gallery at %s with %s photos', self.sPath, len(self.aImgs))
        if len(self.aImgs) > 0:
            self.createThumbs()
            self.createPages()
            self.createIndex()

    def createPages(self):
        """Create a page for each photo"""
        self.log.info('Creating photo pages')
        sTitle = self.getTitle()
        for sImg in self.aImgs:
            sFile = os.path.basename(sImg)
            sCaption = self.getCaption(sFile)
            sPageName = self.sPath + 'pages/' + sFile.replace('.jpg', '.html')

            page = HtmlPage('Gallery - ' + sTitle, self.getStyle())
            tCenter = HtmlTag('center', None)
            tImgLink = LinkHtmlTag('../index.html', None)
            tImgLink.addTag(ImageHtmlTag('../photos/' + sFile, sCaption))
            tCenter.addTag(tImgLink)
            tCenter.addTag(HtmlTag('p', sCaption))
            page.add(tCenter)
            page.save(sPageName)

    def createIndex(self):
        sTitle = self.getTitle()
        dirThumbs = self.sPath + 'thumbs/'
        aImgLinks = []
        for sImg in self.aImgs:
            sFile = os.path.basename(sImg)
            sThumb = dirThumbs + sFile
            sCaption = self.getCaption(sFile)
            sPageName = 'pages/' + sFile.replace('.jpg', '.html')
            tLink = LinkHtmlTag(sPageName, None)
            tLink.addTag(ImageHtmlTag(sThumb, sCaption))
            aImgLinks.append(tLink)

        page = GalleryHtmlPage(sTitle)
        page.addHeading(1, sTitle)
        page.addTable(aImgLinks, self.getPicsPerRow(), True).addAttr('width', '100%').addAttr('cellpadding', '10px')
        page.save(self.sPath + 'index.html')


    def readCaptionsFile(self):
        """If a captions file is found, parse it"""
        sCaptionsFile = self.sPath + 'captions'
        if (os.path.exists(sCaptionsFile)):
            self.dicCaptions = {}
            self.log.info('Parsing captions from %s', sCaptionsFile)
            oFile = open(sCaptionsFile, 'r')  #, encoding="ISO-8859-1")
            while True:
                sLine = oFile.readline()

                aCells = sLine.split('\t')
                if (len(aCells) == 2):
                    self.dicCaptions[aCells[0]] = aCells[1].strip()
                else:
                    self.log.warn('Unexpected captions line %s cells %d', sLine, len(aCells))
                
                # if sLine is empty, end of file is reached
                if not sLine:
                    break
            oFile.close()

    def getCaption(self, sFile):
        if self.dicCaptions:
            if sFile in self.dicCaptions:
                return self.dicCaptions[sFile]
            return ''
        else:
            sCaption = sFile.replace('.jpg', '')
            sCaption = re.sub(r'(\d+)$', r' \1', sCaption)
            sCaption = sCaption.replace('-', ' ')
            return sCaption.capitalize()
    
    def getStyle(self):
        """Get the CSS stylesheet path"""
        return 'http://www.tf79.ch/scripts/style.css'
    
    def getPicsPerRow(self):
        """Number of pictures per row in index page"""
        return 3
    
        
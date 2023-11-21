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
from json import dumps
from HtmlPage import *
from GalleryHtmlPage import *
from Gallery import *

class TF79Gallery(Gallery):
    log = logging.getLogger('TF79Gallery')
    
    def __init__(self, sPath):
        self.sPath = sPath
        self.aImgs = sorted(glob.glob(self.sPath + 'photos/*.jpg'))
        self.dicCaptions = None
        self.sTitle = os.path.basename(sPath)

    def build(self):
        self.readCaptionsFile()
        self.log.info('Building TF79.ch gallery at %s with %s photos', self.sPath, len(self.aImgs))
        if len(self.aImgs) > 0:
            self.createThumbs()
            self.createPages()
            self.createIndex()
            self.createSettingsFile()

    def createPages(self):
        """Create a page for each photo"""
        self.log.info('Creating photo pages')
        sTitle = self.getTitle()

        dirPages = self.sPath + 'pages/'
        if not os.path.exists(dirPages):
            os.makedirs(dirPages)

        for sImg in self.aImgs:
            sFile = os.path.basename(sImg)
            sCaption = self.getCaption(sFile)
            sPageName = dirPages + sFile.replace('.jpg', '.html')

            page = HtmlPage('Galerie &mdash; ' + sTitle, None)
            tCenter = HtmlTag('center', None)
            tImgLink = LinkHtmlTag('../index.html', None)
            tImgLink.addTag(ImageHtmlTag('../photos/' + sFile, sCaption, sCaption))
            tCenter.addTag(tImgLink)
            tCenter.addTag(HtmlTag('p', sCaption))
            page.add(tCenter)
            page.save(sPageName)

    def createIndex(self):
        """Create the gallery index.html page."""
        sTitle = self.sTitle
        dirThumbs = 'thumbs/'
        aImgLinks = []
        for sImg in self.aImgs:
            sFile = os.path.basename(sImg)
            sThumb = dirThumbs + sFile
            sCaption = self.getCaption(sFile)
            sPageName = 'pages/' + sFile.replace('.jpg', '.html')
            tLink = LinkHtmlTag(sPageName, None)
            tLink.addTag(ImageHtmlTag(sThumb, sCaption, sCaption))
            aImgLinks.append(tLink)

        page = GalleryHtmlPage(sTitle)
        page.addHeading(1, sTitle)
        page.addTable(aImgLinks, self.getPicsPerRow(), True).addAttr('width', '100%').addAttr('cellpadding', '10px')
        sComments = self.readCommentsFile()
        if len(sComments) > 0:
            page.add(HtmlTag('div', sComments))
        page.save(self.sPath + 'index.html')
    
    def rename(self, name):
        """Rename pictures in a sequence with the specified name"""
        self.log.info('Renaming photos to %s', name)
        self.sTitle = name
        aImgs = sorted(glob.glob(self.sPath + 'photos/*.JPG'))
        self.log.info('Found %d originals in %s', len(aImgs), self.sPath + 'photos/*.JPG')
        iSeq = 0
        for sOrig in aImgs:
            iSeq += 1
            sNewName = f'{self.sPath}photos/{name}{iSeq:03d}.jpg'
            self.log.info('Renaming %s to %s', sOrig, sNewName)
            os.rename(sOrig, sNewName)

    def createCaptionsFile(self):
        """Create a default captions file"""
        sCaptionsFile = self.sPath + 'captions'
        if (os.path.exists(sCaptionsFile)):
            self.log.info('Captions file exists')
        else:
            self.sTitle = self.getTitle()
            self.log.info('Creating captions file for %s', self.sTitle)
            oFile = open(sCaptionsFile, 'w')
            oFile.write('gallery\t' + self.sTitle + '\n')
            for sImg in self.aImgs:
                oFile.write(os.path.basename(sImg) + '\t\n')
            oFile.close()

    def createSettingsFile(self):
        """Create a default JSON settings file"""
        sJsonFile = self.sPath + 'settings.json'
        if (os.path.exists(sJsonFile)):
            self.log.info('Settings file exists')
        else:
            self.log.info('Creating JSON settings file for %s', self.sTitle)
            settings = {
                'title': self.sTitle,
                'created': int(time.time()),
                'vitrine': None,
                'captions': self.dicCaptions
            }
            oFile = open(sJsonFile, 'w')
            oFile.write(dumps(settings, indent=2))
            oFile.close()

    def readCaptionsFile(self):
        """If a captions file is found, parse it"""
        sCaptionsFile = self.sPath + 'captions'
        self.createCaptionsFile()
        if (os.path.exists(sCaptionsFile)):
            self.dicCaptions = {}
            self.log.info('Parsing captions from %s', sCaptionsFile)
            oFile = open(sCaptionsFile, 'r')  #, encoding="ISO-8859-1")

            for sLine in oFile:
                sLine = sLine.strip('\n')
                #self.log.info(sLine)
                aCells = sLine.split('\t')
                if (len(aCells) == 2):
                    self.dicCaptions[aCells[0]] = aCells[1].strip()
                elif sLine.startswith('gallery'):
                    self.sTitle = sLine.replace('gallery ', '')
                    self.log.info('Title from captions file is ' + self.sTitle)
                else:
                    self.log.warn('Unexpected captions line %s cells %d', sLine, len(aCells))
            oFile.close()

            if 'gallery' in self.dicCaptions:
                self.log.info('Title from captions dict is %s', self.dicCaptions['gallery'])
                self.sTitle = self.dicCaptions['gallery']
                del self.dicCaptions['gallery']

    def readCommentsFile(self):
        """If a comments file is found, parse it"""
        sCommentsFile = self.sPath + 'comments.html'
        sComments = ''
        if (os.path.exists(sCommentsFile)):
            self.log.info('Adding comments from %s', sCommentsFile)
            oFile = open(sCommentsFile, 'r')  #, encoding="ISO-8859-1")
            while True:
                sLine = oFile.readline()
                sComments += sLine
                
                # if sLine is empty, end of file is reached
                if not sLine:
                    break
            oFile.close()
        return sComments

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
    
        
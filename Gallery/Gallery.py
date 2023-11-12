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
import subprocess
from HtmlPage import *

class Gallery:
    log = logging.getLogger('Gallery')
    
    def __init__(self, sPath):
        """Constructor with photo path. Globs the images."""
        self.sPath = sPath
        self.aImgs = sorted(glob.glob(self.sPath + '*.jpg'))
        
    def build(self):
        """Builds the gallery index and thumbnails."""
        self.log.info('Building gallery at %s with %s photos', self.sPath, len(self.aImgs))
        if len(self.aImgs) > 0:
            self.createThumbs()
            self.createIndex()

    def createThumbs(self):
        """Creates thumbnail images if needed."""
        dirThumbs = self.sPath + 'thumbs/'

        if not os.path.exists(dirThumbs):
            os.makedirs(dirThumbs)

        for sImg in self.aImgs:
            sThumb = dirThumbs + os.path.basename(sImg)
            if not os.path.exists(sThumb):
                self.log.info('Creating thumbnail image %s', sThumb)
                sCmd = f'convert {sImg} -resize 180x180 {sThumb}'
                os.system(sCmd)

    def createIndex(self):
        """Creates an HTML gallery index."""
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
        """Returns the gallery title, by capitalizing the directory."""
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
        """Returns the thumbnail path of the first image in this gallery."""
        if len(self.aImgs) > 0:
            sImg = self.aImgs[0]
            sThumb = self.sPath + 'thumbs/' + os.path.basename(sImg)
            return sThumb
        return None
    
    def getImageSizes(self, sImgFile):
        """Returns the [width, height] in pixels of the specified image"""
        result = subprocess.run(['identify', sImgFile], stdout=subprocess.PIPE)
        pattern = re.compile('.+ ([0-9]+x[0-9]+) .+')
        matcher = re.match(pattern, result.stdout.decode('utf-8'))
        if matcher:
            sSizes = matcher.group(1).split('x')
            shape = [int(sSizes[0]), int(sSizes[1])]
            #self.log.info('%s sizes: %s', sImgFile, shape)
            return shape
        else:
            self.log.error('Sizes: no match for %s', result.stdout.decode('utf-8'))
            return None
        
    def resize(self, sSize):
        """Resize images to the specified size, if they are larger."""
        self.log.info('Resizing images to max %spx', sSize)
        iMaxSize = int(sSize)
        for img in self.aImgs:
            shape = self.getImageSizes(img)
            if max(shape) > 1.06*iMaxSize:
                name = os.path.basename(img)
                self.log.info('Resizing %s from %dpx to %dpx', name, max(shape), iMaxSize)
                sCmd = f'convert -size {iMaxSize}x{iMaxSize} {img} -resize {iMaxSize}x{iMaxSize} {img}'
                #self.log.info(sCmd)
                os.system(sCmd)

    def rename(self, name):
        """Rename pictures in a sequence with the specified name"""
        self.sName = name
        pass
    
    def size(self):
        """Returns the number of images in this gallery."""
        return len(self.aImgs)
    

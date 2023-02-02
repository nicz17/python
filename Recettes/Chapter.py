"""A recipe chapter."""

import config
from HtmlPage import *
from RecettesHtmlPage import *

class Chapter:
    def __init__(self, idx, sTitle):
        self.idx = idx
        self.sTitle = sTitle
        self.aRecipes = []

    def addRecipe(self, oRec):
        self.aRecipes.append(oRec)

    def getFilename(self):
        return 'chapter' + str(self.idx) + '.html'

    def toHtml(self):
        """Exports the chapter as an HTML file with a simple list of links."""
        oPage = RecettesHtmlPage(self.sTitle)
        oPage.addHeading(2, self.sTitle)

        aRecLinks = []
        for oRec in self.aRecipes:
            aRecLinks.append(oRec.getSubLink())
        oPage.addList(aRecLinks)

        oPage.save(config.sDirExport + self.getFilename())

    def toHtmlGallery(self):
        """Exports the chapter as an HTML file with a gallery of thumbnails."""
        oPage = RecettesHtmlPage(self.sTitle)
        oPage.addHeading(2, self.sTitle)

        aRecLinks = []
        for oRec in self.aRecipes:
            if oRec.hasPhoto():
                oRec.createThumb()
            tImg = ImageHtmlTag(oRec.getThumbLink(), oRec.sTitle)
            if not oRec.hasThumb():
                tImg = ImageHtmlTag('thumbs/' + config.sDefThumb, oRec.sTitle)
            tName = HtmlTag('p', oRec.sTitle)
            tLink = HtmlTag('a').addAttr('href', 'html/' + oRec.getFilename())
            tLink.addTag(tImg)
            tLink.addTag(tName)
            aRecLinks.append(tLink)
        oPage.addTable(aRecLinks, 4, True).addAttr('width', '800px').addAttr('cellpadding', '20px')

        oPage.save(config.sDirExport + self.getFilename())
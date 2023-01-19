"""A recipe chapter."""

import config
from HtmlPage import *

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
        oPage = HtmlPage(self.sTitle, '../scripts/style.css')
        oPage.addHeading(2, self.sTitle)

        aRecLinks = []
        for oRec in self.aRecipes:
            aRecLinks.append(oRec.getSubLink())
        oPage.addList(aRecLinks)

        oPage.save(config.sDirExport + self.getFilename())
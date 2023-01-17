"""A recipe chapter."""

from HtmlPage import *

class Chapter:
    sDir = 'html/'

    def __init__(self, idx, sTitle):
        self.idx = idx
        self.sTitle = sTitle
        self.aRecipes = []

    def addRecipe(self, oRec):
        self.aRecipes.append(oRec)

    def getFilename(self):
        return self.sDir + 'chapter' + str(self.idx) + '.html'

    def toHtml(self):
        oPage = HtmlPage(self.sTitle, 'style.css')
        oPage.addHeading(2, self.sTitle)

        aRecLinks = []
        for oRec in self.aRecipes:
            aRecLinks.append(oRec.getLink())
        oPage.addList(aRecLinks)

        oPage.save(self.getFilename())
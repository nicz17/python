"""A recipe website builder. Creates various HTML files."""

import datetime
import logging
from HtmlPage import *

class Builder:
    """A recipe website builder. Creates various HTML files."""
    sDir = 'html/'
    log = logging.Logger(__name__)

    def __init__(self):
        self.aRecipes = []
        self.aChapters = []

    def addRecipe(self, oRec):
        """Add a recipe."""
        self.aRecipes.append(oRec)

    def addChapter(self, oChap):
        """Add a chapter."""
        self.aChapters.append(oChap)

    def buildAll(self):
        self.buildRecipes()
        self.buildChapters()
        self.buildHomePage()
        self.buildPhotosPage()

    def buildRecipes(self):
        """Parse the recipes and create their HTML files."""
        self.log.info('Building %d recipes', len(self.aRecipes))
        for oRec in self.aRecipes:
            oRec.parseSource()
            oRec.toHtml()

    def buildChapters(self):
        """Create the chapter HTML files."""
        self.log.info('Building %d chapers', len(self.aChapters))
        for oChap in self.aChapters:
            oChap.toHtml()

    def buildHomePage(self):
        """Build the recipe home page index.html"""
        self.log.info('Building Home page')
        aChapLinks = []
        for oChap in self.aChapters:
            aChapLinks.append(LinkHtmlTag(oChap.getFilename(), oChap.sTitle))

        oPage = HtmlPage('Recettes', 'html/style.css')
        oPage.addHeading(1, 'Les recettes du petit Nicolas')
        oPage.addHeading(2, 'La carte')
        oPage.addList(aChapLinks)

        sNow = datetime.date.today().strftime("%d.%m.%Y")
        oPage.add(HtmlTag('small', 'Compilé le ' + sNow + ' avec ' + str(len(self.aRecipes)) + ' recettes'))

        oPage.save('index.html')

    def buildPhotosPage(self):
        """Build the recipe picture gallery"""
        self.log.info('Building photo gallery')
        oPage = HtmlPage('Photos des recettes', 'style.css')
        oPage.addHeading(1, 'Photos des recettes')
        aTagsThumbs = []
        for oRec in self.aRecipes:
            aTagsThumbs.append(ImageHtmlTag(oRec.getThumb(), oRec.sTitle))
        oPage.addTable(aTagsThumbs, 4)
        oPage.save(self.sDir + 'thumbs.html')

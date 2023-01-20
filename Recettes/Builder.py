"""A recipe website builder. Creates various HTML files."""

import datetime
import time
import logging
import config
from HtmlPage import *
from RecettesHtmlPage import *

class Builder:
    """A recipe website builder. Creates various HTML files."""
    sDir = 'html/'
    log = logging.getLogger(__name__)

    def __init__(self):
        self.aRecipes  = []
        self.aChapters = []
        self.dOrigins  = {}

    def addRecipe(self, oRec):
        """Add a recipe."""
        self.aRecipes.append(oRec)
        
    def addChapter(self, oChap):
        """Add a chapter."""
        self.aChapters.append(oChap)

    def addOrigin(self, sOrigin, oRec):
        if not sOrigin in self.dOrigins:
            self.dOrigins[sOrigin] = []
        self.dOrigins[sOrigin].append(oRec)

    def buildAll(self):
        """Build all HTML pages."""
        self.buildRecipes()
        self.buildChapters()
        self.buildHomePage()
        self.buildPhotosPage()
        self.buildNewsPage()
        self.buildOriginsPage()
        self.buildIngredientsPage()

    def buildRecipes(self):
        """Parse the recipes and create their HTML files."""
        self.log.info('Building %d recipes', len(self.aRecipes))
        for oRec in self.aRecipes:
            oRec.parseSource()
            oRec.toHtml()
            if oRec.sOrigin:
                self.addOrigin(oRec.getOriginCountry(), oRec)

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

        oPage = RecettesHtmlPage('Recettes')
        oPage.addHeading(1, 'Les recettes du petit Nicolas')
        oPage.addHeading(2, 'La carte')
        oPage.addList(aChapLinks)

        sNow = datetime.date.today().strftime("%d.%m.%Y")
        oPage.add(HtmlTag('small', 'Compilé le ' + sNow + ' avec ' + str(len(self.aRecipes)) + ' recettes'))

        oPage.save(config.sDirExport + 'index.html')

    def buildPhotosPage(self):
        """Build the recipe picture gallery"""
        self.log.info('Building photo gallery')
        oPage = RecettesHtmlPage('Photos des recettes')
        oPage.addHeading(1, 'Photos des recettes')
        aTagsThumbs = []
        for oRec in self.aRecipes:
            if oRec.hasPhoto():
                oTagLink = LinkHtmlTag('html/' + oRec.getFilename(), None)
                oTagLink.addTag(ImageHtmlTag(oRec.getThumb(), oRec.sTitle))
                aTagsThumbs.append(oTagLink)
        oPage.addTable(aTagsThumbs, 4).addAttr('width', '100%').addAttr('cellpadding', '20px')
        oPage.save(config.sDirExport + 'thumbs.html')

    def buildNewsPage(self):
        """Build the page of most recent recipes."""
        self.log.info('Building news page')

        # Sort recipes by file creation time
        self.aRecipes.sort(key=lambda rec: rec.getCreatedAt())
        tTableNews = HtmlTag('table')
        for oRec in reversed(self.aRecipes[-10 : ]):
            tRow = HtmlTag('tr')
            sTime = time.strftime('%d.%m.%Y', time.gmtime(oRec.getCreatedAt()))
            tCellDate = HtmlTag('td', sTime).addAttr('class', 'td-ingr-left')
            tCellRec = HtmlTag('td')
            tCellRec.addTag(oRec.getSubLink())
            tRow.addTag(tCellDate)
            tRow.addTag(tCellRec)
            tTableNews.addTag(tRow)

        oPage = RecettesHtmlPage('Nouvelles recettes')
        oPage.addHeading(1, 'Nouvelles recettes')
        oPage.add(tTableNews)
        oPage.save(config.sDirExport + 'news.html')

    def buildOriginsPage(self):
        """Build the recipe origins page."""
        self.log.info('Building origins page')

        oPage = RecettesHtmlPage('Origines des recettes')
        oPage.addHeading(1, 'Origines des recettes')

        aOrigins = []
        for sOrigin in sorted(self.dOrigins.keys()):
            aRecLinks = []
            for oRec in self.dOrigins[sOrigin]:
                aRecLinks.append(oRec.getSubLink())
            tOrigin = InlineHtmlTag(sOrigin + ' : ', aRecLinks, ', ')
            aOrigins.append(tOrigin)

        oPage.addList(aOrigins)
        oPage.save(config.sDirExport + 'origins.html')

    def buildIngredientsPage(self):
        """Build the ingredients page."""
        self.log.info('Building ingredients page')

        oPage = RecettesHtmlPage('Ingrédients')
        oPage.addHeading(1, 'Ingrédients')
        oPage.save(config.sDirExport + 'ingredients.html')


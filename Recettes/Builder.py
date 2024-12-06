"""A recipe website builder. Creates various HTML files."""

import datetime
import time
import logging
import config
import os
import re
import json
from Chapter import *
from FileReader import *
from Recipe import *
from HtmlPage import *
from RecettesHtmlPage import *
from Timer import *
import TextTools

class Builder:
    """A recipe website builder. Creates various HTML files."""
    sDir = 'html/'
    log = logging.getLogger(__name__)

    def __init__(self):
        self.aRecipes  = []
        self.aChapters = []
        self.dOrigins  = {}
        self.dIngreds  = {}
        self.oTimer = Timer()

    def parseChapters(self):
        """Parse the main chapters LaTeX file."""
        sFileChapters = config.sDirSources + 'chapitres.tex'
        self.log.info('Reading %s', sFileChapters)
        if not os.path.exists(sFileChapters):
            self.log.error('Missing chapters file %s, aborting', sFileChapters)
            exit('Abort')

        oFileReader = FileReader(sFileChapters, 'ISO-8859-1')
        iChapter = 0
        oChap = None
        oPatternChap = re.compile('\\\\chapitre\{(.+)\}')
        oPatternRec  = re.compile('\\\\(include|input)\{(.+)\}')
        for sLine in oFileReader:
            # Parse chapters
            oMatch = re.match(oPatternChap, sLine)
            if (oMatch):
                iChapter += 1
                sTitle = oMatch.group(1)
                oChap = Chapter(iChapter, sTitle)
                self.addChapter(oChap)

            # Parse recipe includes
            oMatch = re.match(oPatternRec, sLine)
            if (oMatch):
                sName = oMatch.group(2)
                oRec = Recipe(sName, oChap)
                oChap.addRecipe(oRec)
                self.addRecipe(oRec)
                
        oFileReader.close()
        self.log.info('Found %d chapters', iChapter)

    def addRecipe(self, oRec: Recipe):
        """Add a recipe."""
        self.aRecipes.append(oRec)
        
    def addChapter(self, oChap: Chapter):
        """Add a chapter."""
        self.aChapters.append(oChap)

    def addOrigin(self, sOrigin: str, oRec: Recipe):
        """Add a recipe origin country."""
        if not sOrigin in self.dOrigins:
            self.dOrigins[sOrigin] = []
        self.dOrigins[sOrigin].append(oRec)

    def addIngredient(self, sIngr: str, oRec: Recipe):
        """Add a recipe ingredient."""
        if not sIngr in self.dIngreds:
            self.dIngreds[sIngr] = []
        self.dIngreds[sIngr].append(oRec)

    def buildAll(self):
        """Build all HTML pages."""
        self.buildRecipes()
        self.buildChapters()
        self.buildHomePage()
        self.buildPhotosPage()
        self.buildNewsPage()
        self.buildOriginsPage()
        self.buildIngredientsPage()
        self.buildJson()
        self.log.info('Done building in %s', self.oTimer.getElapsed())

    def buildRecipes(self):
        """Parse the recipes and create their HTML files."""
        self.log.info('Building %d recipes', len(self.aRecipes))
        for oRec in self.aRecipes:
            oRec.parseSource()
            oRec.toHtml()
            if oRec.sOrigin:
                self.addOrigin(oRec.getOriginCountry(), oRec)
            for sIngr in oRec.aIngrLinks:
                self.addIngredient(sIngr, oRec)

    def buildChapters(self):
        """Create the chapter HTML files."""
        self.log.info('Building %d chapers', len(self.aChapters))
        for oChap in self.aChapters:
            #oChap.toHtml()
            oChap.toHtmlGallery()

    def buildHomePage(self):
        """Build the recipe home page index.html"""
        self.log.info('Building Home page')

        aChapters = []
        for oChap in self.aChapters:
            aChapters.append(LinkHtmlTag(oChap.getFilename(), oChap.sTitle))

        aLinks = []
        aLinks.append(LinkHtmlTag('readme.html', 'Quelques indications utiles'))
        aLinks.append(LinkHtmlTag('thumbs.html', 'Photos'))
        aLinks.append(LinkHtmlTag('ingredients.html', 'Ingrédients'))
        aLinks.append(LinkHtmlTag('origins.html', 'Origines des recettes'))
        aLinks.append(LinkHtmlTag('news.html', 'Nouveautés'))
        aLinks.append(LinkHtmlTag('liens.html', 'Liens culinaires'))
        aLinks.append(LinkHtmlTag('thanks.html', 'Remerciements'))
        aLinks.append(LinkHtmlTag('biblio.html', 'Bibliographie'))

        oPage = RecettesHtmlPage('Recettes')
        oPage.includeScript('http://www.tf79.ch/recettes/recs.js')
        oPage.addHeading(1, 'Les recettes du petit Nicolas')
        tDivCarte = BlueBoxHtmlTag('La carte')
        tDivCarte.addTag(ListHtmlTag(aChapters))
        tDivRight = DivHtmlTag()
        tDivLinks = BlueBoxHtmlTag('Tables et liens')
        tDivLinks.addTag(ListHtmlTag(aLinks))
        tDivRight.addTag(tDivLinks)
        sNow = datetime.date.today().strftime("%d.%m.%Y")
        tDivRight.addTag(HtmlTag('p', '<br><br>Compilé le ' + sNow + ' avec ' + str(len(self.aRecipes)) + ' recettes'))
        oPage.add(TableHtmlTag((tDivCarte, tDivRight), 2, 'top').addAttr('width', '1050px'))

        # Random recipes
        tDivRandom = BlueBoxWideHtmlTag('Quelques recettes')
        tTableRandom = HtmlTag('table').addAttr('width', '800px').addAttr('cellpadding', '20px')
        tRowRandom = HtmlTag('tr')
        tRowRandom.addTag(ScriptHtmlTag('randomRecs();'))
        tTableRandom.addTag(tRowRandom)
        tDivRandom.addTag(tTableRandom)
        oPage.add(tDivRandom)

        oPage.save(config.sDirExport + 'index.html')

    def buildPhotosPage(self):
        """Build the recipe picture gallery"""
        self.log.info('Building photo gallery')
        aTagsThumbs = []
        aTagsNoPic = []
        for oRec in self.aRecipes:
            if oRec.hasPhoto():
                #oRec.createThumb()
                oTagLink = LinkHtmlTag('html/' + oRec.getFilename(), None)
                oTagLink.addTag(ImageHtmlTag(oRec.getThumbLink(), oRec.sTitle))
                aTagsThumbs.append(oTagLink)
            else:
                aTagsNoPic.append(oRec.getSubLink())

        oPage = RecettesHtmlPage('Photos des recettes')
        oPage.addHeading(1, 'Photos des recettes')
        oPage.addTable(aTagsThumbs, 4, True).addAttr('width', '100%').addAttr('cellpadding', '20px')
        oPage.addHeading(2, 'Recettes sans photo')
        oPage.addList(aTagsNoPic)
        oPage.save(config.sDirExport + 'thumbs.html')

    def buildNewsPage(self):
        """Build the page of most recent recipes."""
        self.log.info('Building news page')

        # Sort recipes by file creation time
        self.aRecipes.sort(key=lambda rec: rec.getCreatedAt())
        tTableNews = HtmlTag('table')
        for oRec in reversed(self.aRecipes[-8 : ]):
            tRow = HtmlTag('tr')
            sTime = time.strftime('%d.%m.%Y', time.gmtime(oRec.getCreatedAt()))
            tCellDate = HtmlTag('td', sTime).addAttr('class', 'td-pad-r')
            tCellRec = HtmlTag('td').addAttr('class', 'td-pad-r')
            tCellRec.addTag(oRec.getSubLink())
            tCellChange = HtmlTag('td')
            tCellChange.addTag(HtmlTag('font', oRec.sChangeLog).addAttr('color', 'grey'))
            tRow.addTag(tCellDate)
            tRow.addTag(tCellRec)
            tRow.addTag(tCellChange)
            tTableNews.addTag(tRow)

        oPage = RecettesHtmlPage('Recettes - Derniers changements')
        oPage.addHeading(1, 'Derniers changements')
        oPage.add(tTableNews)
        oPage.save(config.sDirExport + 'news.html')

    def buildOriginsPage(self):
        """Build the recipe origins page."""
        self.log.info('Building origins page with %d countries', len(self.dOrigins))

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
        """Build the ingredients page, separated by initial letter."""
        self.log.info('Building ingredients page with %d ingredients', len(self.dIngreds))

        oPage = RecettesHtmlPage('Ingrédients')
        oPage.menu.addTag(HtmlTag('h2', 'Ingrédients'))
        tableMenu = TableHtmlTag([], 4)
        tableMenu.addAttr('width', '120px')
        oPage.menu.addTag(tableMenu)
        oPage.addHeading(1, 'Ingrédients')

        def sortLowerCase(s):
            return TextTools.replaceAccents(s).lower()

        aIngreds = []
        sLetterCurr = None
        for sIngr in sorted(self.dIngreds.keys(), key=sortLowerCase):
            sLetter = sIngr[0:1].upper()
            if not sLetter == sLetterCurr:
                if len(aIngreds) > 0:
                    oPage.addList(aIngreds)
                oPage.addHeading(2, '<a name="' + sLetter + '">' + sLetter + '</a>')
                tableMenu.getNextCell().addTag(LinkHtmlTag(f'#{sLetter}', sLetter))
                sLetterCurr = sLetter
                aIngreds = []

            aRecLinks = []
            for oRec in self.dIngreds[sIngr]:
                aRecLinks.append(oRec.getSubLink())
            sWikiLink = '<a href="http://fr.wikipedia.org/wiki/' + sIngr + '" target="_blank">'
            sWikiLink += sIngr + '</a>'
            tIngr = InlineHtmlTag(sWikiLink + ' : ', aRecLinks, ', ')
            aIngreds.append(tIngr)

        oPage.addList(aIngreds)
        oPage.save(config.sDirExport + 'ingredients.html')

    def buildJson(self):
        self.log.info('Exporting recipes to Json')
        aRecs = []
        for oRec in self.aRecipes:
            if oRec.hasPhoto():
                dRecipe = {}
                dRecipe['sName']  = oRec.sName
                dRecipe['sTitle'] = oRec.sTitle
                aRecs.append(dRecipe)
        sJson = json.dumps(aRecs, indent=2)
        oFile = open('recs.json', 'w', encoding="ISO-8859-1")
        oFile.write(sJson)
        oFile.close()



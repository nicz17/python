"""A recipe."""

import os
import re
import config
from HtmlPage import *

class Ingredient:
    """An ingredient quantity and name."""
    def __init__(self, sQuantity, sName):
        self.sQuantity = sQuantity
        self.sName = sName

    def getTableRow(self):
        return HtmlTag('tr', '<td class="td-ingr-left">' + self.sQuantity + '</td><td>' + self.sName + '</td>')

class IngredientTableHtmlTag(HtmlTag):
    """An HTML table specialized for the recipe ingredients."""
    def __init__(self, aIngredients):
        super().__init__('table', None)
        for ingr in aIngredients:
            self.addTag(ingr.getTableRow())

class Recipe:
    sDir = 'html/'

    def __init__(self, sName):
        self.sName = sName
        self.sTitle = 'Title not parsed'
        self.sSubtitle = None
        self.sOrigin = None
        self.aIngr = []
        self.aText = []

    def parseSource(self):
        """Reads the recipe source LaTeX file."""
        sFile = config.sDirSources + self.sName + '.tex'
        if not os.path.exists(sFile):
            print('ERROR: file not found', sFile)

        oFile = open(sFile, 'r', encoding="ISO-8859-1")
        iLine = 0
        sText = ''
        oPatternRec      = re.compile('\\\\recette\{(.+)\}')
        oPatternIngr     = re.compile('(.+)\& (.+)\\\\\\\\')
        oPatternSubtitle = re.compile('\\\\emph\{(.+)\}')
        oPatternIndex    = re.compile('\\\\index\{(.+)\}\{(.+)\}')
        oPatternIgnore   = re.compile('\\\\(label|begin|end|changelog|source)\{.+')
        while True:
            iLine += 1
            sLine = oFile.readline()

            # if sLine is undefined, end of file is reached
            if not sLine:
                break

            # Ignored some lines
            oMatch = re.match(oPatternIgnore, sLine)
            if (oMatch):
                continue

            # Parse recipe title
            oMatch = re.match(oPatternRec, sLine)
            if (oMatch):
                self.sTitle = oMatch.group(1)
                continue

            # Parse recipe subtitle
            oMatch = re.match(oPatternSubtitle, sLine)
            if (oMatch):
                self.sSubtitle = HtmlTag('i', oMatch.group(1))
                continue

            # Replace LaTeX stuff
            sLine = self.replace(sLine)

            # Parse index
            oMatch = re.match(oPatternIndex, sLine)
            if (oMatch):
                # TODO handle index
                sIndexName = oMatch.group(1)
                sKey = oMatch.group(2)
                if (sIndexName == 'pays'):
                    self.sOrigin = sKey
                continue

            # Parse ingredients
            oMatch = re.match(oPatternIngr, sLine)
            if (oMatch):
                self.aIngr.append(Ingredient(oMatch.group(1).strip(), oMatch.group(2)))
                continue

            # End paragraphs on empty lines
            if not sLine.strip():
                if len(sText) > 0:
                    self.aText.append(HtmlTag('p', sText))
                    sText = ''
                continue

            # Add text instructions
            sText += sLine.strip() + ' '

        oFile.close()

        # Add final paragraph
        if len(sText) > 0:
            self.aText.append(HtmlTag('p', sText))

    def replace(self, str):
        str = re.sub(r"\\\`a", 'à', str)
        str = re.sub(r"\\\^a", 'â', str)
        str = re.sub(r"\\\^e", 'ê', str)
        str = re.sub(r"\\\'e", 'é', str)
        str = re.sub(r"\\\^i", 'î', str)
        str = re.sub(r"\\\"i", 'ï', str)
        str = re.sub(r"\\(-|noindent|bigskip|medskip|smallskip|pagebreak)", '', str)
        str = re.sub(r"\\oe ", '&oelig;', str)
        str = re.sub(r"\\undemi", '&frac12;', str)
        str = re.sub(r'\\emph\{(.+)\}', r'<i>\1</i>', str)
        str = re.sub(r'\\ingr\{(.+)\}', r'<a href="index.ingr.html">\1</a>', str)
        str = re.sub(r'page~\\pageref\{rec:(.+)\}', r'<a href="\1.html">recette</a>', str)
        return str

    def getLink(self):
        """Returns a HTML link to this recipe."""
        return LinkHtmlTag(self.sName + '.html', self.sTitle)

    def getFilename(self):
        """Returns the recipe HTML file name."""
        return self.sDir + self.sName + '.html'

    def getPhoto(self):
        """Returns the recipe photo filename."""
        return config.sDirPhotos + self.sName + '.jpg'

    def toHtml(self):
        """Builds the recipe HTML page."""
        oPage = HtmlPage(self.sTitle, 'style.css')
        oPage.addHeading(1, self.sTitle)

        if self.sSubtitle:
            oPage.add(self.sSubtitle)

        aTablePhoto = []
        tDivIngr = DivHtmlTag('ingr')
        tDivIngr.addAttr('align', 'center')
        tDivIngr.addTag(IngredientTableHtmlTag(self.aIngr))
        aTablePhoto.append(tDivIngr)
        aTablePhoto.append(ImageHtmlTag(self.getPhoto(), self.sTitle, 'Pas encore de photo'))
        oPage.addTable(aTablePhoto, 2).addAttr('width', '100%')

        for oPar in self.aText:
            oPage.add(oPar)

        if self.sOrigin:
            tDivOrigin = DivHtmlTag('recPays')
            tDivOrigin.addTag(LinkHtmlTag('index.pays.html', 'Origine : ' + self.sOrigin))
            oPage.add(tDivOrigin)

        oPage.save(self.getFilename())
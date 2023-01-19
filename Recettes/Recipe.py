"""A recipe."""

import os
import re
import config
import logging
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
    log = logging.getLogger('Recipe')
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
            self.log.error('File not found: %s', sFile)
            exit('Aborted')

        oFile = open(sFile, 'r', encoding="ISO-8859-1")
        iLine = 0
        sText = ''
        oPatternRec      = re.compile('\\\\recette\{(.+)\}')
        oPatternIngr     = re.compile('(.+)\& (.+)\\\\\\\\')
        oPatternIngrNQ   = re.compile('\& (.+)\\\\\\\\')
        oPatternSubtitle = re.compile('\\\\emph\{(.+)\}')
        oPatternVariante = re.compile('\\\\variante\{(.+)\}')
        oPatternIndex    = re.compile('\\\\index\{(.+)\}\{(.+)\}')
        oPatternIgnore   = re.compile('\\\\(label|begin|end|changelog|source)\{.+')
        oPatternComment  = re.compile('%.+')
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
            oMatch = re.match(oPatternComment, sLine)
            if (oMatch):
                continue

            # Parse recipe title
            oMatch = re.match(oPatternRec, sLine)
            if (oMatch):
                self.sTitle = self.replace(oMatch.group(1))
                continue

            # Parse recipe subtitle
            oMatch = re.match(oPatternSubtitle, sLine)
            if (oMatch):
                self.sSubtitle = HtmlTag('p')
                self.sSubtitle.addTag(HtmlTag('i', self.replace(oMatch.group(1))))
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
            oMatch = re.match(oPatternIngrNQ, sLine)
            if (oMatch):
                self.aIngr.append(Ingredient('', oMatch.group(1)))
                continue

            # Add variations
            oMatch = re.match(oPatternVariante, sLine)
            if (oMatch):
                self.aText.append(HtmlTag('h2', 'Variante : ' + oMatch.group(1)))
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
        str = re.sub(r"\\\`A", '&Agrave;', str)
        str = re.sub(r"\\\`a", 'à', str)
        str = re.sub(r"\\\^a", 'â', str)
        str = re.sub(r"\\\'E", '&Eacute;', str)
        str = re.sub(r"\\\^e", 'ê', str)
        str = re.sub(r"\\\'e", 'é', str)
        str = re.sub(r"\\\`e", 'è', str)
        str = re.sub(r"\\\^i", 'î', str)
        str = re.sub(r"\\\"i", 'ï', str)
        str = re.sub(r"\\\^o", 'ô', str)
        str = re.sub(r"\\\^u", 'û', str)
        str = re.sub(r"\\(-|noindent|bigskip|medskip|smallskip|pagebreak)", '', str)
        str = re.sub(r"\\oe ", '&oelig;', str)
        str = re.sub(r"\\c\{c\}", '&ccedil;', str)
        str = re.sub(r"\\undemi", '&frac12;', str)
        str = re.sub(r'\\emph\{(.+)\}', r'<i>\1</i>', str)
        str = re.sub(r'\\ingr\{(.+)\}', r'<a href="index.ingr.html">\1</a>', str)
        str = re.sub(r'page.\\pageref\{rec:(.+)\}', r'<a href="\1.html">recette</a>', str)
        return str

    def getCreatedAt(self):
        oFile = config.sDirSources + self.sName + '.tex'
        return os.path.getmtime(oFile)

    def getLink(self):
        """Returns a HTML link to this recipe in same dir."""
        return LinkHtmlTag(self.sName + '.html', self.sTitle)

    def getSubLink(self):
        """Returns a HTML link to this recipe under html/."""
        return LinkHtmlTag(self.getFilename(), self.sTitle)

    def getFilename(self):
        """Returns the recipe HTML file name."""
        return self.sDir + self.sName + '.html'

    def getPhoto(self):
        """Returns the recipe photo filename."""
        return config.sDirPhotos + self.sName + '.jpg'

    def hasPhoto(self):
        return os.path.exists(self.getPhoto())

    def getThumb(self):
        """Returns the recipe thumbnail filename."""
        return config.sDirThumbs + self.sName + '.jpg'

    def toHtml(self):
        """Builds the recipe HTML page."""
        oPage = HtmlPage(self.sTitle, 'style.css')
        oPage.addHeading(1, self.sTitle)

        if self.sSubtitle:
            oPage.add(self.sSubtitle)

        tDivIngr = DivHtmlTag('ingr')
        tDivIngr.addAttr('align', 'center')
        tDivIngr.addTag(IngredientTableHtmlTag(self.aIngr))
        tTable = HtmlTag('table').addAttr('width', '100%')
        tRow = HtmlTag('tr')
        tCellIngr = HtmlTag('td').addAttr('valign', 'top')
        tCellIngr.addTag(tDivIngr)
        tCellPhoto = HtmlTag('td').addAttr('width', '500px').addAttr('align', 'right')
        tCellPhoto.addTag(ImageHtmlTag(self.getPhoto(), self.sTitle, 'Pas encore de photo'))
        tRow.addTag(tCellIngr)
        tRow.addTag(tCellPhoto)
        tTable.addTag(tRow)
        oPage.add(tTable)

        for oPar in self.aText:
            oPage.add(oPar)

        if self.sOrigin:
            tDivOrigin = DivHtmlTag('recPays')
            tDivOrigin.addTag(LinkHtmlTag('index.pays.html', 'Origine : ' + self.sOrigin))
            oPage.add(tDivOrigin)

        oPage.save(self.getFilename())
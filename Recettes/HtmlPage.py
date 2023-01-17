"""
 An HTML page generator
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

class HtmlPage:
    def __init__(self, sTitle, sStyle):
        self.sTitle = sTitle
        self.html = HtmlTag('html')
        self.head = HtmlTag('head')
        self.body = HtmlTag('body')
        self.html.addTag(self.head)
        self.html.addTag(self.body)

        self.buildHead(sStyle)
        self.buildBody()

    def buildHead(self, sStyle):
        self.head.addTag(HtmlTag('title', self.sTitle))

        tStyle = HtmlTag('link')
        tStyle.addAttr('rel', "stylesheet")
        tStyle.addAttr('type', "text/css")
        tStyle.addAttr('href', sStyle)
        self.head.addTag(tStyle)

        tScript = HtmlTag('script')
        tScript.addAttr('src', 'http://www.tf79.ch/scripts/tf79.js')
        self.head.addTag(tScript)

    def buildBody(self):
        self.menu = DivHtmlTag('menu')
        self.body.addTag(self.menu)
        self.menu.addTag(HtmlTag('h1', '<a href="http://www.tf79.ch/index.html">Accueil</a>'))
        self.menu.addTag(HtmlTag('h3', '<a href="http://www.tf79.ch/bookmarks.html">Favoris</a>'))
        self.menu.addTag(HtmlTag('h3', '<a href="http://www.tf79.ch/nature/index.html">Nature</a>'))
        self.menu.addTag(HtmlTag('h1', '<a href="../index.html">Recettes</a>'))
        self.menu.addTag(HtmlTag('h3', '<a href="../news.html">Nouveautés</a>'))
        self.menu.addTag(HtmlTag('h3', '<a href="../readme.html">Aide</a>'))

        self.main = DivHtmlTag('main')
        self.body.addTag(self.main)

        self.body.addTag(HtmlTag('script', 'createFooter();'))

    def add(self, tag):
        """Adds the specified tag to the main div."""
        self.main.addTag(tag)

    def addHeading(self, iLevel, sTitle):
        self.main.addTag(HtmlTag('h' + str(iLevel), sTitle))

    def addList(self, aItems):
        tUl = HtmlTag('ul')
        for item in aItems:
            tLi = HtmlTag('li')
            tLi.addTag(item)
            tUl.addTag(tLi)
        self.main.addTag(tUl)

    def addTable(self, aItems, nItemsByRow = 4):
        tTable = HtmlTag('table')
        tRow = None
        nItemsInRow = 0
        for item in aItems:
            if (nItemsInRow % nItemsByRow == 0):
                tRow = HtmlTag('tr')
                tTable.addTag(tRow)
            tCell = HtmlTag('td')
            tRow.addTag(tCell)
            tCell.addTag(item)
            nItemsInRow += 1
        self.main.addTag(tTable)
        return tTable

    def save(self, sFilename):
        print('Saving', self.__str__(), 'as', sFilename)
        oFile = open(sFilename, 'w')
        oFile.write('<!DOCTYPE html>\n' + self.html.getHtml())

    def __str__(self):
        return 'HtmlPage ' + self.sTitle

class HtmlTag:
    def __init__(self, sName, sContent = None):
        self.sName = sName
        self.sContent = sContent
        self.tags = []
        self.attrs = {}

    def getHtml(self, depth=0):
        html = self.getIndent(depth) + '<' + self.sName
        for attr in self.attrs:
            html += ' ' + attr + '="' + self.attrs[attr] + '"'
        html += '>'
        if (self.sContent):
            html += self.sContent
        else:
            html += '\n'
        for tag in self.tags:
            html += tag.getHtml(depth+1)
        
        if (self.needEndTag()):
            if (self.sContent == None):
                html += self.getIndent(depth)
            html += '</' + self.sName + '>\n'
        return html

    def addTag(self, tag):
        self.tags.append(tag)

    def addAttr(self, sName, sValue):
        self.attrs[sName] = sValue

    def getIndent(self, depth):
        return '  ' * depth

    def needEndTag(self):
        return self.sName != 'link' and self.sName != 'img'

    def __str__(self):
        return 'HtmlTag ' + self.sName

class DivHtmlTag(HtmlTag):
    def __init__(self, sId=None, sClass=None):
        super().__init__('div')
        if sId:
            self.addAttr('id', sId)
        if sClass:
            self.addAttr('class', sClass)

class ImageHtmlTag(HtmlTag):
    def __init__(self, sSource, sTitle, sAlt = None):
        super().__init__('img', None)
        self.addAttr('src', sSource)
        self.addAttr('title', sTitle)
        if sAlt:
            self.addAttr('alt', sAlt)

class LinkHtmlTag(HtmlTag):
    def __init__(self, sRef, sText):
        super().__init__('a', sText)
        self.addAttr('href', sRef)

class TableHtmlTag(HtmlTag):
    def __init__(self, aItems, nItemsByRow = 4):
        super().__init__('table', None)
        tRow = None
        nItemsInRow = 0
        for item in aItems:
            if (nItemsInRow % nItemsByRow == 0):
                tRow = HtmlTag('tr')
                self.addTag(tRow)
            tCell = HtmlTag('td', item)
            tRow.addTag(tCell)
            #tCell.addTag(item)
            nItemsInRow += 1


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

        tTitle = HtmlTag('title', sTitle)
        self.head.addTag(tTitle)

        tStyle = HtmlTag('link')
        tStyle.addAttr('rel', "stylesheet")
        tStyle.addAttr('type', "text/css")
        tStyle.addAttr('href', sStyle)
        self.head.addTag(tStyle)

        self.main = HtmlTag('div')
        self.main.addAttr('id', 'main')
        self.body.addTag(self.main)

    def add(self, tag):
        self.main.addTag(tag)

    def addHeading(self, iLevel, sTitle):
        self.main.addTag(HtmlTag('h' + str(iLevel), sTitle))

    def addList(self, aItems):
        tUl = HtmlTag('ul')
        for item in aItems:
            tUl.addTag(HtmlTag('li', item))
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

class ImageHtmlTag(HtmlTag):
    def __init__(self, sSource, sTitle):
        super().__init__('img', None)
        self.addAttr('src', sSource)
        self.addAttr('title', sTitle)
        self.addAttr('alt', sTitle)

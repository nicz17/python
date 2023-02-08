"""
 An HTML page generator
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging

class HtmlPage:
    """An HTML page."""
    log = logging.getLogger('HtmlPage')

    def __init__(self, sTitle, sStyle = 'style.css'):
        self.sTitle = sTitle
        self.html = HtmlTag('html')
        self.head = HtmlTag('head')
        self.body = HtmlTag('body')
        self.html.addTag(self.head)
        self.html.addTag(self.body)

        self.buildHead(sStyle)
        self.buildBody()

    def buildHead(self, sStyle):
        """Build the HTML head tag with CSS style, scripts etc."""
        self.head.addTag(HtmlTag('title', self.sTitle))

        tStyle = HtmlTag('link')
        tStyle.addAttr('rel', "stylesheet")
        tStyle.addAttr('type', "text/css")
        tStyle.addAttr('href', sStyle)
        self.head.addTag(tStyle)

    def buildBody(self):
        """Build HTML body tag with main div and possible menu div."""
        self.buildHeader()
        self.menu = DivHtmlTag('menu')
        self.buildMenu()

        self.main = DivHtmlTag('main')
        self.body.addTag(self.main)

        self.buildFooter()

    def buildHeader(self):
        """Build the HTML header div on top"""
        pass

    def buildMenu(self):
        """Build the HTML menu div on the left"""
        pass

    def buildFooter(self):
        """Build the HTML footer div at the bottom"""
        pass

    def add(self, tag):
        """Adds the specified tag to the main div."""
        self.main.addTag(tag)

    def includeScript(self, sUrl):
        tScript = HtmlTag('script').addAttr('src', sUrl)
        self.head.addTag(tScript)

    def addHeading(self, iLevel, sTitle):
        """Add a heading of the specified level, for example h1."""
        self.main.addTag(HtmlTag('h' + str(iLevel), sTitle))

    def addList(self, aItems):
        """Add a UL list to the main div."""
        self.main.addTag(ListHtmlTag(aItems))

    def addTable(self, aItems, nItemsByRow = 4, bCenterCells = False):
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
            if (bCenterCells):
                tCell.addAttr('align', 'center')
            nItemsInRow += 1
        self.main.addTag(tTable)
        return tTable

    def save(self, sFilename):
        self.log.info('Saving %s as %s', self.__str__(), sFilename)
        oFile = open(sFilename, 'w', encoding="ISO-8859-1")
        oFile.write('<!DOCTYPE html>' + self.html.getHtml())
        oFile.close()

    def __str__(self):
        return 'HtmlPage ' + self.sTitle

class HtmlTag:
    """A generic HTML tag, with attributes, content and child tags."""
    def __init__(self, sName, sContent = None):
        """Constructor with tag name and optional content."""
        self.sName = sName
        self.sContent = sContent
        self.tags = []
        self.attrs = {}

    def getHtml(self, depth=0, bInline = False):
        """Build this tag's HTML string."""
        html = ''
        # newline and indent
        if not bInline:
            html += '\n' + self.getIndent(depth)

        # open tag and attributes
        html += '<' + self.sName
        for attr in self.attrs:
            html += ' ' + attr + '="' + self.attrs[attr] + '"'
        html += '>'

        # own content
        if self.sContent:
            html += self.sContent

        # children tags
        nChildren = self.countChildren()
        for tag in self.tags:
            html += tag.getHtml(depth+1, nChildren < 2)
        
        # end tag
        if self.needEndTag():
            if self.sContent == None and nChildren > 1:
                html += '\n' + self.getIndent(depth)
            html += '</' + self.sName + '>'

        return html

    def addTag(self, tag):
        """Add a child tag."""
        self.tags.append(tag)

    def addAttr(self, sName, sValue):
        """Add an attribute and its value."""
        self.attrs[sName] = sValue
        return self

    def getIndent(self, depth):
        return '  ' * depth

    def needEndTag(self):
        return self.sName != 'link' and self.sName != 'img'
    
    def countChildren(self):
        count = len(self.tags)
        for tag in self.tags:
            count += tag.countChildren()
        return count

    def __str__(self):
        return 'HtmlTag ' + self.sName

class DivHtmlTag(HtmlTag):
    def __init__(self, sId=None, sClass=None):
        super().__init__('div')
        if sId:
            self.addAttr('id', sId)
        if sClass:
            self.addAttr('class', sClass)

class BlueBoxHtmlTag(DivHtmlTag):
    """A div tag with myBox class."""
    def __init__(self, sTitle, sId=None):
        super().__init__(sId, 'blueBox')
        self.addTag(HtmlTag('h2', sTitle))

class BlueBoxWideHtmlTag(DivHtmlTag):
    """A div tag with myBox class."""
    def __init__(self, sTitle, sId=None):
        super().__init__(sId, 'blueBox blueBox-wide')
        self.addTag(HtmlTag('h2', sTitle))

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
    def __init__(self, aItems, nItemsByRow = 4, valign = None):
        super().__init__('table', None)
        tRow = None
        nItemsInRow = 0
        for item in aItems:
            if (nItemsInRow % nItemsByRow == 0):
                tRow = HtmlTag('tr')
                self.addTag(tRow)
            tCell = HtmlTag('td')
            if valign:
                tCell.addAttr('valign', valign)
            if isinstance(item, str):
                tCell = HtmlTag('td', item)
            else:
                tCell.addTag(item)
            tRow.addTag(tCell)
            nItemsInRow += 1

class ListHtmlTag(HtmlTag):
    def __init__(self, aItems):
        super().__init__('ul')
        for item in aItems:
            tLi = HtmlTag('li')
            if isinstance(item, str):
                tLi = HtmlTag('li', item)
            else:
                tLi.addTag(item)
            self.addTag(tLi)

class GrayFontHtmlTag(HtmlTag):
    def __init__(self, sContent):
        super().__init__('font', sContent)
        self.addAttr('color', 'gray')

class ScriptHtmlTag(HtmlTag):
    """A JavaScript tag with its code."""
    def __init__(self, sCode):
        super().__init__('script', sCode)

class InlineHtmlTag(HtmlTag):
    """An HTML tag displaying its contents on a single line."""
    def __init__(self, sContent, aItems, sSeparator):
        super().__init__('span', sContent)
        self.aItems = aItems
        self.sSeparator = sSeparator

    def getHtml(self, depth=0, bInline = False):
        html = ''
        if not bInline:
            html += self.getIndent(depth)
        if self.sContent:
            html += self.sContent
        bFirst = True
        for oItem in self.aItems:
            if bFirst:
                bFirst = False
            else:
                html += self.sSeparator
            if isinstance(oItem, str):
                html += oItem
            else:
                html += oItem.getHtml(0, True)
        if not bInline:
            html += '\n'
        return html
    
class HtmlComment(HtmlTag):
    def __init__(self, sComment):
        super().__init__('c', None)
        self.sComment = sComment
    def getHtml(self, depth=0, bInline = False):
        html = '\n' + self.getIndent(depth)
        html += '<!-- ' + self.sComment + ' -->'
        return html

def testInlineTag():
    print('Testing InlineHtmlTag')
    oPage = HtmlPage('Test inline')
    aItems = ['one', 'two', LinkHtmlTag('google.com', 'Google'), 'three']
    oPage.addHeading(1, 'Inline tag test')
    oPage.add(InlineHtmlTag('List: ', aItems, ' - '))
    oPage.save('test.html')

if __name__ == '__main__':
    testInlineTag()

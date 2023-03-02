"""
 An HTML page specialized for galleries at http://www.tf79.ch/gallery/
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
import time
from HtmlPage import *

class GalleryHtmlPage(HtmlPage):
    log = logging.getLogger('GalleryHtmlPage')

    def __init__(self, sTitle, sPath = ''):
        self.sPath = sPath
        self.sGalleryTitle = sTitle
        super().__init__('TF79.ch - Galeries - ' + sTitle, 'http://www.tf79.ch/scripts/style.css')
        sTime = time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))
        self.head.addTag(HtmlComment('Generated by gallery.py on ' + sTime))
        self.head.addTag(MetaHtmlTag('author', 'Nicolas Zwahlen'))
        self.includeScript('http://www.tf79.ch/scripts/tf79.js')

    def buildHeader(self):
        tDivHeader = DivHtmlTag('header')
        tDivHeader.addTag(HtmlTag('small', 'TF79.ch &mdash; Galeries'))
        self.body.addTag(tDivHeader)

    def buildMenu(self):
        self.menu = DivHtmlTag('menu')
        self.body.addTag(self.menu)
        self.menu.addTag(HtmlTag('h1', '<a href="http://www.tf79.ch/index.html">Accueil</a>'))
        self.menu.addTag(HtmlTag('h3', '<a href="http://www.tf79.ch/bookmarks.html">Favoris</a>'))
        self.menu.addTag(HtmlTag('h3', '<a href="http://www.tf79.ch/nature/index.html">Nature</a>'))
        self.menu.addTag(HtmlTag('h3', '<a href="http://www.tf79.ch/recettes/index.html">Recettes</a>'))
        self.menu.addTag(HtmlTag('h3', '<a href="http://www.tf79.ch/divers/index.html">Divers</a>'))
        self.menu.addTag(HtmlTag('h1', '<a href="http://www.tf79.ch/gallery/index.html">Galeries</a>'))
        self.menu.addTag(HtmlTag('h3', self.sGalleryTitle))

    def buildFooter(self):
        self.body.addTag(ScriptHtmlTag('createFooter();'))

    def addMenuLink(self, sLink, sName):
        """Adds a menu link."""
        self.menu.addTag(HtmlTag('h3', '<a href="' + self.sPath + sLink + '">' + sName + '</a>'))
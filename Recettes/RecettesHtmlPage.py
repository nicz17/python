"""
 An HTML page specialized for recipes at http://www.tf79.ch/recettes/
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
from HtmlPage import *

class RecettesHtmlPage(HtmlPage):
    log = logging.getLogger('RecettesHtmlPage')

    def __init__(self, sTitle, sPath = ''):
        self.sPath = sPath
        super().__init__(sTitle, sPath + '../scripts/style.css')

    def buildMenu(self):
        self.menu = DivHtmlTag('menu')
        self.body.addTag(self.menu)
        self.menu.addTag(HtmlTag('h1', '<a href="http://www.tf79.ch/index.html">Accueil</a>'))
        self.menu.addTag(HtmlTag('h3', '<a href="http://www.tf79.ch/bookmarks.html">Favoris</a>'))
        self.menu.addTag(HtmlTag('h3', '<a href="http://www.tf79.ch/nature/index.html">Nature</a>'))
        self.menu.addTag(HtmlTag('h1', '<a href="' + self.sPath + 'index.html">Recettes</a>'))
        self.menu.addTag(HtmlTag('h3', '<a href="' + self.sPath + 'news.html">Nouveautés</a>'))
        self.menu.addTag(HtmlTag('h3', '<a href="' + self.sPath + 'thumbs.html">Photos</a>'))
        self.menu.addTag(HtmlTag('h3', '<a href="' + self.sPath + 'readme.html">Aide</a>'))
        self.menu.addTag(HtmlTag('h3', '<a href="' + self.sPath + 'biblio.html">Bibliographie</a>'))

    def addChapterLink(self, sLink, sName):
        """Adds a chapter link to the menu."""
        self.menu.addTag(HtmlTag('h3', '<a href="' + self.sPath + sLink + '">' + sName + '</a>'))

#!/usr/bin/env python3

"""
 A recipe website generator
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import re
import config
from HtmlPage import *
from Chapter import *
from Recipe import *

sFileChapters = config.sDirSources + 'chapitres.tex'

def readChapters():
    print('Reading', sFileChapters)
    aRecipes = []
    aChapters = []
    oChap = None

    oFile = open(sFileChapters, 'r', encoding="ISO-8859-1")
    iLine = 0
    iChapter = 0
    oPatternChap = re.compile('\\\\chapitre\{(.+)\}')
    oPatternRec  = re.compile('\\\\include\{(.+)\}')
    while True:
        iLine += 1
        sLine = oFile.readline()
        #print('Line', iLine, sLine.strip())

        # Parse chapters
        oMatch = re.match(oPatternChap, sLine)
        if (oMatch):
            iChapter += 1
            sTitle = oMatch.group(1)
            #print('Line', iLine, 'new chapter:', sTitle)
            oChap = Chapter(iChapter, sTitle)
            aChapters.append(oChap)

        # Parse recipe includes
        oMatch = re.match(oPatternRec, sLine)
        if (oMatch):
            sName = oMatch.group(1)
            oRec = Recipe(sName)
            aRecipes.append(oRec)
            oChap.addRecipe(oRec)
        
        # if sLine is empty, end of file is reached
        if not sLine:
            break

    oFile.close()
    print('Found', len(aChapters), 'chapters and', len(aRecipes), 'recipes')

    for oRec in aRecipes:
        oRec.parseSource()
        oRec.toHtml()

    aChapLinks = []
    for oChap in aChapters:
        oChap.toHtml()
        aChapLinks.append(LinkHtmlTag(oChap.getFilename(), oChap.sTitle))

    # Build index.html
    oPage = HtmlPage('Recettes', 'html/style.css')
    oPage.addHeading(1, 'Les recettes du petit Nicolas')
    oPage.addHeading(2, 'La carte')
    oPage.addList(aChapLinks)
    oPage.add(HtmlTag('p', str(len(aRecipes)) + ' recettes'))
    oPage.save('index.html')


def main():
    print('Welcome to Recettes v' + __version__)
    readChapters()

main()

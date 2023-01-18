#!/usr/bin/env python3

"""
 A recipe website generator
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import re
import config
import logging
from Builder import *
from HtmlPage import *
from Chapter import *
from Recipe import *

sFileChapters = config.sDirSources + 'chapitres.tex'

def configureLogging():
    """
    Configures logging to have timestamped logs at INFO level
    on stdout and in a log file.
    """
    
    logging.basicConfig(
        format = '%(asctime)s %(levelname)s %(name)s: %(message)s',
        datefmt = '%Y.%m.%d %H:%M:%S',
        level = logging.INFO,
        handlers = [
            logging.FileHandler("recettes.log"),
            logging.StreamHandler()
        ])
    return logging.getLogger('Recettes')

def readChapters(oBuilder):
    """Parse the main chapters LaTeX file."""

    log.info('Reading %s', sFileChapters)
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
            oBuilder.addChapter(oChap)

        # Parse recipe includes
        oMatch = re.match(oPatternRec, sLine)
        if (oMatch):
            sName = oMatch.group(1)
            oRec = Recipe(sName)
            oChap.addRecipe(oRec)
            oBuilder.addRecipe(oRec)
        
        # if sLine is empty, end of file is reached
        if not sLine:
            break

    oFile.close()

def main():
    print('Welcome to Recettes v' + __version__)
    builder = Builder()
    readChapters(builder)
    builder.buildAll()

log = configureLogging()
main()

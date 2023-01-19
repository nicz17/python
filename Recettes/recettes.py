#!/usr/bin/env python3

"""
 A recipe website generator
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import os
import re
import config
import logging
from Builder import *
from HtmlPage import *
from Chapter import *
from Recipe import *


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

def checkConfig():
    """Checks that config dirs exist."""

    if not os.path.exists(config.sDirSources):
        log.error('Missing LaTeX source dir %s, aborting', config.sDirSources)
        exit('Abort')
    if not os.path.exists(config.sDirPhotos):
        log.error('Missing photo dir %s, aborting', config.sDirPhotos)
        exit('Abort')
    if not os.path.exists(config.sDirThumbs):
        log.error('Missing thumbs dir %s, aborting', config.sDirThumbs)
        exit('Abort')

def readChapters(oBuilder):
    """Parse the main chapters LaTeX file."""

    sFileChapters = config.sDirSources + 'chapitres.tex'
    log.info('Reading %s', sFileChapters)
    if not os.path.exists(sFileChapters):
        log.error('Missing chapters file %s, aborting', sFileChapters)
        exit('Abort')

    oFile = open(sFileChapters, 'r', encoding="ISO-8859-1")
    iLine = 0
    iChapter = 0
    oChap = None
    oPatternChap = re.compile('\\\\chapitre\{(.+)\}')
    oPatternRec  = re.compile('\\\\(include|input)\{(.+)\}')
    while True:
        iLine += 1
        sLine = oFile.readline()

        # Parse chapters
        oMatch = re.match(oPatternChap, sLine)
        if (oMatch):
            iChapter += 1
            sTitle = oMatch.group(1)
            #log.debug('Line %d new chapter: %s', iLine, sTitle)
            oChap = Chapter(iChapter, sTitle)
            oBuilder.addChapter(oChap)

        # Parse recipe includes
        oMatch = re.match(oPatternRec, sLine)
        if (oMatch):
            sName = oMatch.group(2)
            oRec = Recipe(sName, oChap)
            oChap.addRecipe(oRec)
            oBuilder.addRecipe(oRec)
        
        # if sLine is empty, end of file is reached
        if not sLine:
            break

    oFile.close()

def main():
    log.info('Welcome to Recettes v' + __version__)
    checkConfig()

    builder = Builder()
    readChapters(builder)
    builder.buildAll()

log = configureLogging()
main()

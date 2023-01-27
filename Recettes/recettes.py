#!/usr/bin/env python3

"""
 A recipe website generator.
 This is the main entry point.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import os
import sys
import config
import logging
import getopt
from Builder import *
from Uploader import *


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

def getOptions():
    """Parse program arguments and store them in a dict."""
    dOptions = {'debug': False, 'upload': False, 'open': False}
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hduo", ["help", "debug", "upload", 'open'])
    except getopt.GetoptError:
        print("Invalid options: %s", sys.argv[1:])
    for opt, arg in opts:
        log.info("Parsing option %s value %s", opt, arg)
        if opt in ('-h', '--help'):
            print('recettes.py --help --debug --upload')
            sys.exit()
        elif opt in ("-d", "--debug"):
            dOptions['debug'] = True
        elif opt in ("-u", "--upload"):
            dOptions['upload'] = True
        elif opt in ("-o", "--open"):
            dOptions['open'] = True
    return dOptions

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

def main():
    """Main function. Builds or uploads depending on options."""
    log.info('Welcome to Recettes v' + __version__)
    checkConfig()

    if (dOptions['upload']):
        uploader = Uploader()
        uploader.test()
        #uploader.uploadAll()
    else:
        builder = Builder()
        builder.parseChapters()
        builder.buildAll()

    if dOptions['open']:
        # Display home page in browser
        os.system('firefox ' + config.sDirExport + 'index.html')

log = configureLogging()
dOptions = getOptions()
main()

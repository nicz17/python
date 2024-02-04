#!/usr/bin/env python3

"""
 Helper scripts for Panorpa.
 This is the main entry point.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import os
import sys
#import config
import logging
import getopt
from CopyFromCamera import *
from GeoTracker import *
from PynorpaApp import *
#from LocationCache import *
#from Uploader import *


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
            logging.FileHandler("pynorpa.log"),
            logging.StreamHandler()
        ])
    return logging.getLogger('Pynorpa')

def getOptions():
    """Parse program arguments and store them in a dict."""
    dOptions = {'dryrun': False, 'upload': False, 'open': False, 'copy': False}
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hduoc", ["help", "dry", "upload", 'open', 'copy'])
    except getopt.GetoptError:
        print("Invalid options: %s", sys.argv[1:])
    for opt, arg in opts:
        log.info("Parsing option %s value %s", opt, arg)
        if opt in ('-h', '--help'):
            print('pynorpa.py -h (help) -u (upload) -d (upload dry run) -o (open in browser) -c (copy from D800)')
            sys.exit()
        elif opt in ("-d", "--dry"):
            dOptions['dryrun'] = True
        elif opt in ("-u", "--upload"):
            dOptions['upload'] = True
        elif opt in ("-o", "--open"):
            dOptions['open'] = True
        elif opt in ("-c", "--copy"):
            dOptions['copy'] = True
    return dOptions

def checkConfig():
    """Checks that config dirs exist."""
    pass

def main():
    """Main function. Builds or uploads depending on options."""
    log.info('Welcome to Pynorpa v' + __version__)
    checkConfig()

    if (dOptions['copy']):
        copier = CopyFromCamera()
        copier.loadImages()
        copier.copyImages()
        tracker = GeoTracker()
        tracker.prepare()
        tracker.copyFiles()
        tracker.loadGeoTracks()
        tracker.setPhotoGPSTags()
        tracker.buildHtmlPreviews()
    else:
        app = PynorpaApp()
        app.run()

log = configureLogging()
dOptions = getOptions()
main()

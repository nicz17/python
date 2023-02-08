#!/usr/bin/env python3

"""
 A gallery generator.
 This is the main entry point.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import os
import sys
import logging
import getopt
from Gallery import *
from MultiGallery import *


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
            logging.StreamHandler()
        ])
    return logging.getLogger('Gallery')

def getOptions():
    """Parse program arguments and store them in a dict."""
    dOptions = {'dir': '.', 'resize': False, 'open': False, 'all': False}
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:ora", ["help", "dir=", "resize", 'open', 'all'])
    except getopt.GetoptError:
        print("Invalid options: %s", sys.argv[1:])
    for opt, arg in opts:
        log.info("Parsing option %s value %s", opt, arg)
        if opt in ('-h', '--help'):
            print('gallery.py -h (help) -r (resize) -d (dir) -o (open in browser)')
            sys.exit()
        elif opt in ("-d", "--dir"):
            dOptions['dir'] = arg
        elif opt in ("-r", "--resize"):
            dOptions['resize'] = True
        elif opt in ("-o", "--open"):
            dOptions['open'] = True
        elif opt in ("-a", "--all"):
            dOptions['all'] = True
    return dOptions

def main():
    """Main function. Builds or uploads depending on options."""
    log.info('Welcome to Gallery v%s', __version__)
    
    if dOptions['all']:
        multiGal = MultiGallery(dOptions['dir'])
        multiGal.build()
    else:
        gal = Gallery(dOptions['dir'])
        gal.build()

log = configureLogging()
dOptions = getOptions()
main()

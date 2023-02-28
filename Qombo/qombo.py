#!/usr/bin/env python3

"""
 A small merge game
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import sys
import logging
import getopt
from QomboApp import *


def configureLogging():
    """
    Configures logging to have timestamped logs at INFO level
    on stdout and in a log file.
    """
    
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
        level=logging.INFO,
        datefmt = '%Y.%m.%d %H:%M:%S',
        handlers=[logging.StreamHandler()])
    return logging.getLogger('Qombo')

def getOptions():
    """Parse program arguments and store them in a dict."""
    dOptions = {'open': False, 'gui': False}
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hox", ["help", 'open', 'gui'])
    except getopt.GetoptError:
        print("Invalid options: %s", sys.argv[1:])
    for opt, arg in opts:
        log.info("Parsing option %s value %s", opt, arg)
        if opt in ('-h', '--help'):
            print('orfact.py -h (help) -o (open in browser)')
            sys.exit()
        elif opt in ("-o", "--open"):
            dOptions['open'] = True
        elif opt in ("-x", "--gui"):
            dOptions['gui'] = True
    return dOptions

def main():
    log.info('Welcome to Qombo v' + __version__)
    app = QomboApp()
    app.run()
    

log = configureLogging()
dOptions = getOptions()
main()

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
from TF79Gallery import *
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
    dOptions = {'dir': '.', 'name': None, 'resize': None, 'open': False, 'all': False, 'tf79': False}
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:n:r:oat", ["help", "dir=", "name=", "resize=", 'open', 'all', 'tf79'])
    except getopt.GetoptError:
        print("Invalid options: %s", sys.argv[1:])
    for opt, arg in opts:
        log.info("Parsing option %s value %s", opt, arg)
        if opt in ('-h', '--help'):
            print('gallery.py -h (help) -r (resize) -d (dir) -n (rename) -a (all galleries in dir) -o (open in browser) -t (TF79 style)')
            sys.exit()
        elif opt in ("-d", "--dir"):
            dOptions['dir'] = arg
        elif opt in ("-n", "--name"):
            dOptions['name'] = arg
        elif opt in ("-r", "--resize"):
            dOptions['resize'] = arg
        elif opt in ("-o", "--open"):
            dOptions['open'] = True
        elif opt in ("-a", "--all"):
            dOptions['all'] = True
        elif opt in ("-t", "--tf79"):
            dOptions['tf79'] = True
    return dOptions

def main():
    """Main function. Builds or uploads depending on options."""
    log.info('Welcome to Gallery v%s', __version__)
    
    if dOptions['all']:
        multiGal = MultiGallery(dOptions['dir'], dOptions['tf79'])
        multiGal.build()
    else:
        gal = None
        if (dOptions['tf79']):
            gal = TF79Gallery(dOptions['dir'])
        else:
            gal = Gallery(dOptions['dir'])

        if (dOptions['name'] is not None):
            gal.rename(dOptions['name'])
            exit()
        if (dOptions['resize'] is not None):
            gal.resize(dOptions['resize'])
            #exit()
        gal.build()

    if dOptions['open']:
        os.system('firefox ' + dOptions['dir'] + 'index.html')

log = configureLogging()
dOptions = getOptions()
main()

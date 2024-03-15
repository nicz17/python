#!/usr/bin/env python3

"""
 Simple UML parser and code generator.
 Reads a text file to generate python or C++ stubs.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import getopt
import sys
from SettingsLoader import *
from SimpleUMLClass import *
from SimpleUMLParser import *


def getOptions():
    """Parse program arguments and store them in a dict."""
    dOptions = {'dir': '.', 'file': None, 'lang': 'python', 'settings': None}
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:f:l:s:", ["help", "dir=", "file=", "lang=", "sett="])
    except getopt.GetoptError:
        print("Invalid options: %s", sys.argv[1:])
    for opt, arg in opts:
        #log.info("Parsing option %s value %s", opt, arg)
        if opt in ('-h', '--help'):
            print('simpleUML.py -h (help) -d (output dir) -f (.uml file) -l (language) -s (settings)')
            sys.exit()
        elif opt in ("-d", "--dir"):
            dOptions['dir'] = arg
        elif opt in ("-f", "--file"):
            dOptions['file'] = arg
        elif opt in ("-l", "--lang"):
            dOptions['lang'] = arg
        elif opt in ("-s", "--sett"):
            dOptions['settings'] = arg
    return dOptions

def configureLogging():
    """ Configures logging to have timestamped logs at INFO level on stdout. """
    logging.basicConfig(
        format = '%(asctime)s %(levelname)s %(name)s: %(message)s',
        datefmt = '%Y.%m.%d %H:%M:%S',
        level = logging.INFO,
        handlers = [logging.StreamHandler()])
    return logging.getLogger('SimpleUML')

def main():
    """Main function. Runs the parser."""
    log.info('Welcome to SimpleUML v' + __version__)
    
    dSettings = None
    if (dOptions['settings']):
        loader = SettingsLoader(dOptions['settings'])
        loader.loadSettings()
        #dSettings = loader.getSettingsDict()
    
    if (dOptions['file']):
        log.info('Parsing %s to generate %s code', dOptions['file'], dOptions['lang'])
        parser = SimpleUMLParser(dOptions['lang'])
        parser.parse(dOptions['file'])
    else:
        log.error('Please enter a .uml file name with -f')

log = configureLogging()
dOptions = getOptions()
main()

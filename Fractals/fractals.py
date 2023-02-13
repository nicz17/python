#!/usr/bin/env python3

"""
 A fractal generator.
 This is the main entry point.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import os
import sys
import logging
import getopt
from FractalsApp import *

sAppName = 'Fractals'

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
    return logging.getLogger(sAppName)


def main():
    """Main function. Builds or uploads depending on options."""
    log.info('Welcome to %s v%s', sAppName, __version__)
    
    app = FractalsApp(sAppName + ' v' + __version__)

log = configureLogging()
#dOptions = getOptions()
main()
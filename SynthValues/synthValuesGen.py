#!/usr/bin/env python3

"""
Generate synthetic values in Pandas dataframes,
according to some model.
Save the data to a CSV file.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
import getopt
import sys
from Model import *


def configureLogging():
    """
    Configures logging to have timestamped logs at INFO level on stdout.
    """
    
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
        level=logging.INFO,
        datefmt = '%Y.%m.%d %H:%M:%S',
        handlers=[logging.StreamHandler()])
    return logging.getLogger('SynthValuesGen')

def getOptions():
    """Parse program arguments and store them in a dict."""

    dOptions = {'plot': False, 'verbose': False}
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hpv', ['help', 'plot', 'verbose'])
    except getopt.GetoptError:
        print("Invalid options: %s", sys.argv[1:])
    for opt, arg in opts:
        log.info("Parsing option %s value %s", opt, arg)
        if opt in ('-h', '--help'):
            print('synthValuesGen.py -h (help) -p (plot) -v (verbose)')
            sys.exit()
        elif opt in ("-v", "--verbose"):
            dOptions['verbose'] = True
        elif opt in ("-p", "--plot"):
            dOptions['plot'] = True
    return dOptions

def main():
    """Main routine."""
    log.info('Welcome to synthValuesGen v' + __version__)
    #model = RandomModel(30, dOptions)
    #model = ConstantModel(30, 100.0, dOptions)
    model = ConsumptionModel(7*96, 30.0, 100.0, dOptions)
    model.createDataframe()
    model.saveAsCSV()

    if dOptions['plot']:
        model.plot()

log = configureLogging()
dOptions = getOptions()
main()
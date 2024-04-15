#!/usr/bin/env python3

"""
 Script pour automatiser la synthèse
 des commandes groupées de céréales.

 Librairies nécessaires:
 pip3 install pandas
 pip3 install openpyxl
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2024 N. Zwahlen"
__version__ = "1.0.0"

import logging
import getopt
import glob
import os
import sys
import pandas as pd


class OrderReader():
    """
    Read order Excel files, extract relevant data, 
    and merge it into the synthesis table.
    """
    log = logging.getLogger("OrderReader")

    def __init__(self, path: str):
        """Constructor."""
        self.path = path
        self.orders = []

    def loadOrders(self):
        """Load order .xls files from path."""
        self.log.info('Loading orders from %s', self.path)
            
        # Check path exists
        if not os.path.exists(self.path):
            self.log.error('Invalid path %s', self.path)
            exit()
        
        # Glob .xls files in path
        self.orders = sorted(glob.glob(self.path + '*.xlsx'))
        self.log.info('Found %d order files:', len(self.orders))
        for order in self.orders:
            self.log.info('  %s', os.path.basename(order))

    def mergeOrders(self):
        """Read order files and merge into the synthesis table."""
        self.log.info('Reading %d order files:', len(self.orders))
        dfMerged = pd.DataFrame()
        for order in self.orders:
            dfOrder = pd.read_excel(order)
            #print(dfOrder)
            name = dfOrder.iloc[2][3]
            if pd.isna(dfOrder.iloc[2, 3]):
                name = os.path.basename(order)
            quant = dfOrder.iloc[6:26, 3]
            self.log.info('Order by "%s"', name)
            dfMerged.insert(0, name, quant)
        #print(dfMerged)
        dfMerged.to_csv('synthese.csv')

    def __str__(self):
        str = "OrderReader"
        str += f' path: {self.path}'
        str += f' orders: {len(self.orders)}'
        return str
      

def configureLogging():
    """
    Configures logging to have timestamped logs at INFO level
    on stdout and in a log file.
    """
    
    logging.basicConfig(
        format = '%(asctime)s %(levelname)s %(name)s: %(message)s',
        datefmt = '%Y.%m.%d %H:%M:%S',
        level = logging.INFO,
        handlers = [logging.StreamHandler()])
    return logging.getLogger('Synthese')

def getOptions():
    """Parse program arguments and store them in a dict."""
    dOptions = {'path': None}
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:', ['help', 'path'])
    except getopt.GetoptError:
        print("Invalid options: %s", sys.argv[1:])
    for opt, arg in opts:
        log.info("Parsing option %s value %s", opt, arg)
        if opt in ('-h', '--help'):
            print('synthese.py -h (help) -p (chemin vers les commandes)')
            sys.exit()
        elif opt in ("-p", "--path"):
            dOptions['path'] = arg
    return dOptions

def main():
    """Main function. Reads XLS files and builds the synthesis."""
    log.info('Bienvenue dans le script de synthèse des commandes')
    log.info('Chemin: %s', dOptions['path'])

    reader = OrderReader(dOptions['path'])
    reader.loadOrders()
    reader.mergeOrders()


log = configureLogging()
dOptions = getOptions()
main()
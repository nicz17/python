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

    def __init__(self, path: str, debug=False):
        """Constructor."""
        self.path = path
        self.debug = debug
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
        iRowFrom = 7
        iRowTo = 27
        iOrder = 1
        for order in self.orders:
            dfOrder = pd.read_excel(order)
            if iOrder == 1:
                rowNames = dfOrder.iloc[iRowFrom:iRowTo, 1]
                rowNames.at[-1] = 'Subsides'
                dfMerged.insert(0, 'Produits', rowNames)
            if self.debug:
                print(dfOrder)
            name = dfOrder.iloc[3][5]  # [row][col]
            if self.debug:
                self.log.info('Name cell is %s', name)
            hasSubsidy = 'avec subside' in order
            if pd.isna(dfOrder.iloc[3, 5]):
                # Hope to find name in filename
                name = os.path.basename(order)
                name = name.replace('formulaire', '')
                name = name.replace('commandes groupees avril 2025', '')
                name = name.replace('sans subside', '')
                name = name.replace('avec subside', '')
                name = name.replace('.xlsx', '')
                name = name.replace(' - ', '')
                name = name.replace('-', '')
                name = name.replace('_', '')
                name = name.strip()
            #hasSubsidy = not pd.isna(dfOrder.iloc[0, 0])
            quant = dfOrder.iloc[iRowFrom:iRowTo, 5]
            quant.at[-1] = 'x' if hasSubsidy else ''
            self.log.info('Commande %s subsides par "%s"', 
                        'AVEC' if hasSubsidy else 'sans', name)
            dfMerged.insert(iOrder, name, quant)
            iOrder += 1
        print(dfMerged)
        dfMerged.to_csv('synthese.csv')
        dfMerged.to_excel('synthese-brute.xlsx')

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
    dOptions = {'path': None, 'debug': False}
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hdp:', ['help', 'debug', 'path'])
    except getopt.GetoptError:
        print("Invalid options: %s", sys.argv[1:])
    for opt, arg in opts:
        log.info("Parsing option %s value %s", opt, arg)
        if opt in ('-h', '--help'):
            print('synthese.py -h (help) -p (chemin vers les commandes)')
            sys.exit()
        elif opt in ("-p", "--path"):
            dOptions['path'] = arg
        elif opt in ("-d", "--debug"):
            dOptions['debug'] = True
    return dOptions

def main():
    """Main function. Reads XLS files and builds the synthesis."""
    log.info('Bienvenue dans le script de synthèse des commandes')
    log.info('Chemin: %s', dOptions['path'])

    if not dOptions['path']:
        log.error('Entrez le chemin vers les commandes avec -p')
        exit()

    reader = OrderReader(dOptions['path'])
    reader.loadOrders()
    reader.mergeOrders()


log = configureLogging()
dOptions = getOptions()
main()
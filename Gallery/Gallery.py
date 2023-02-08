"""
 A photo gallery.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import os
import sys
import logging
import glob

class Gallery:
    log = logging.getLogger('Gallery')
    
    def __init__(self, sPath):
        self.sPath = sPath
        
    def build(self):
        self.log.info('Building gallery at %s', self.sPath)
        aImgs = glob.glob(self.sPath + '*.jpg')
        self.log.info('Found %d photos', len(aImgs))

        
    

"""
Parse a Pynorpa photo selection file.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2026 N. Zwahlen"
__version__ = "1.0.0"

import logging
import os
import re

import TextTools
from pynorpaManager import PynorpaManager
from taxon import TaxonCache

    
class SelectionParser:
    """Parse a Pynorpa photo selection file."""
    log = logging.getLogger('SelectionParser')
    dictAbbr = {
        'coleo': 'coleoptera',
        'het': 'heteroptera',
        'hym': 'hymenoptera',
        'lepi': 'lepidoptera'
    }

    def __init__(self, filename: str, dir: str):
        self.filename = filename
        self.dir = dir
        self.cache = None
        self.manager = None

    def parse(self, dryrun=True):
        self.log.info(f'Parsing {self.filename}')

        # Check file exists
        if not os.path.exists(self.filename):
            self.log.error(f'File does not exist: {self.filename}')
            return None
        
        # Read file
        self.manager = PynorpaManager()
        self.cache = TaxonCache()
        nPhotos = 0
        with open(self.filename, 'r') as file:
            for line in file:
                # TODO find date from header
                ids = re.findall(r'\d+', line.strip())
                if ids and line.startswith(ids[0]):
                    tokens = line.strip().split(' ')
                    name = ''
                    for token in tokens:
                        if not token in ids:
                            name += token + ' '
                    ids = self.completeIds(ids)
                    self.log.debug(f'{" ".join(ids)}: {name}')
                    for id in ids:
                        self.selectFile(id, name, dryrun)
                        nPhotos += 1
        self.log.info(f'Selecting {nPhotos} photos')

    def selectFile(self, id: str, name: str, dryrun: bool):
        """Select a photo."""
        filenameOrig = self.getOrigFilename(id)
        filenameSel  = self.getSelFilename(id, name.strip())

        if not os.path.exists(filenameOrig):
            self.log.error(f'Missing orig file {filenameOrig}')
            return
        if os.path.exists(filenameSel):
            self.log.error(f'Selected file already exists: {filenameSel}')
            return
        
        self.manager.runSystemCommand(f'cp {filenameOrig} {filenameSel}', dryrun)

    def getSelFilename(self, id: str, name: str):
        """Get the selected photo filename from the id and name."""

        fname = name.replace(" ", "-")
        taxon = self.cache.findByName(TextTools.upperCaseFirst(name))
        if not taxon:
            # get taxon name from incomplete latin name
            taxon = self.cache.findByPartialName(name)
        if not taxon:
            # get taxon name from french name
            taxon = self.cache.findByPartialName(name, True)

        if taxon:
            self.log.info(f'Name matches {taxon}')
            fname = self.manager.getBaseFilename(taxon)
        else:
            fname = self.replaceAbbr(name).replace(" ", "-")
        return f'{self.dir.replace("/orig", "/photos")}/{fname}{id}.jpg'

    def getOrigFilename(self, id: str):
        """Get the original photo filename from the id number."""
        return f'{self.dir}/_NZW{id}.JPG'
    
    def replaceAbbr(self, name: str):
        """Replace some common abbreviations."""
        for key in self.dictAbbr:
            name = name.replace(key, self.dictAbbr[key])
        return name

    def completeIds(self, ids: list[str]):
        """Complete 9510, 11 into 9510, 9511."""
        id0 = ids[0]
        result = [id0]
        for id in ids[1:]:
            if len(id) < len(id0):
                #self.log.info(f'Incomplete id {id} base {id0}')
                id = id0[0:len(id0)-len(id)] + id
            result.append(id)
        return result

    def __str__(self):
        return f'SelectionParser for {self.filename}'
    

def testSelectionParser():
    """Unit test for SelectionParser class."""
    cache = TaxonCache()
    cache.load()
    sp = SelectionParser('Nature-2024-01/Kandersteg.txt', 'Nature-2025-05/orig')
    sp.parse()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.DEBUG, handlers=[logging.StreamHandler()])
    testSelectionParser()
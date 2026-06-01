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
from taxon import TaxonCache, Taxon

    
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

    def parse(self, dryrun=True):
        self.log.info(f'Parsing {self.filename}')

        # Check file exists
        if not os.path.exists(self.filename):
            self.log.error(f'File does not exist: {self.filename}')
            return None
        
        # Read file
        self.cache = TaxonCache()
        with open(self.filename, 'r') as file:
            for line in file:
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

    def selectFile(self, id: str, name: str, dryrun: bool):
        """Select a photo."""
        filenameOrig = self.getOrigFilename(id)
        filenameSel  = self.getSelFilename(id, name.strip())
        self.log.info(f'cp {filenameOrig} {filenameSel}')

    def getSelFilename(self, id: str, name: str):
        """Get the selected photo filename from the id and name."""

        taxon = self.cache.findByName(TextTools.upperCaseFirst(name))
        if taxon:
            # TODO get taxon name from latin (manager)
            self.log.info(f'Name matches {taxon}')
            fname = name.replace(" ", "-")
        else:
            # TODO get taxon name from french
            # TODO get taxon name from family name
            fname = self.replaceAbbr(name).replace(" ", "-")
        return f'{self.dir}/photos/{fname}{id}.jpg'

    def getOrigFilename(self, id: str):
        """Get the original photo filename from the id number."""
        return f'{self.dir}/orig/_NZW{id}.JPG'
    
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
    sp = SelectionParser('Nature-2024-01/Kandersteg.txt', 'Nature-2025-05')
    sp.parse()

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.DEBUG, handlers=[logging.StreamHandler()])
    testSelectionParser()
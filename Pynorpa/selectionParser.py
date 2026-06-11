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
from taxon import TaxonCache, Taxon


class SelectedPhoto:
    """Container for a selected orig photo."""
    log = logging.getLogger('SelectedPhoto')

    def __init__(self, id, input: str, orig: str, sel: str, taxon: Taxon, error=None):
        self.id = id
        self.input = input
        self.orig = orig
        self.sel = sel
        self.taxon = taxon
        self.error = error

    def getId(self) -> str:
        return self.id
    
    def getInput(self) -> str:
        return self.input

    def getOrigFilename(self) -> str:
        return self.orig
    
    def getSelFilename(self) -> str:
        return self.sel
    
    def getTaxon(self) -> Taxon:
        return self.taxon
    
    def getTaxonName(self) -> str:
        if self.taxon:
            return self.taxon.getNameFr()
        return ''
    
    def getError(self) -> str:
        return self.error
    
    def hasError(self) -> bool:
        return self.error is not None
    
    def getSummary(self) -> str:
        if self.error:
            return self.error
        return os.path.basename(self.getSelFilename())

    def __str__(self):
        sTaxonFr = '' if self.taxon is None else f' ({self.taxon.getNameFr()})'
        return f'SelectedPhoto {self.id} {self.sel + sTaxonFr if self.sel else self.error}'


class SelectionParser:
    """Parse a Pynorpa photo selection file."""
    log = logging.getLogger('SelectionParser')
    dictAbbr = {
        'coleo': 'coleoptera',
        'het': 'heteroptera',
        'hym': 'hymenoptera',
        'lepi': 'lepidoptera',
        'geom': 'geometridae'
    }

    def __init__(self, filename: str, dir: str):
        self.filename = filename
        self.dir = dir
        self.cache = None
        self.manager = None

    def parse(self, dryrun=True) -> list[SelectedPhoto]:
        self.log.info(f'Parsing {self.filename}')
        result = []

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
                        info = self.selectFile(id, name.strip(), dryrun)
                        result.append(info)
                        nPhotos += 1
        self.log.info(f'Selecting {nPhotos} photos')
        return result

    def selectFile(self, id: str, name: str, dryrun: bool) -> SelectedPhoto:
        """Select a photo."""
        taxon = self.getSelTaxon(name)
        filenameOrig = self.getOrigFilename(id)
        filenameSel  = self.getSelFilename(id, name, taxon)

        if not os.path.exists(filenameOrig):
            self.log.error(f'Missing orig file {filenameOrig}')
            return SelectedPhoto(id, name, None, None, taxon, f'Original manquant : {os.path.basename(filenameOrig)}')
        if os.path.exists(filenameSel):
            self.log.error(f'Selected file already exists: {filenameSel}')
            return SelectedPhoto(id, name, None, None, taxon, f'La photo existe: {os.path.basename(filenameSel)}')
        return SelectedPhoto(id, name, filenameOrig, filenameSel, taxon)

    def getSelTaxon(self, name: str) -> Taxon:
        """Get the selected taxon from the input name, or None."""
        name = self.replaceAbbr(name)
        taxon = self.cache.findByName(TextTools.upperCaseFirst(name))
        if not taxon:
            # get taxon name from incomplete latin name
            taxon = self.cache.findByPartialName(name)
        if not taxon:
            # get taxon name from french name
            taxon = self.cache.findByPartialName(name, True)
        return taxon

    def getSelFilename(self, id: str, name: str, taxon: Taxon):
        """Get the selected photo filename from the id and name."""
        fname = name.replace(" ", "-")
        if taxon:
            self.log.info(f'Name matches {taxon}')
            fname = self.manager.getBaseFilename(taxon)
        else:
            fname = self.replaceAbbr(name).replace(" ", "-")
            #fname = name.replace(" ", "-")
        return f'{self.dir.replace("/orig", "/photos")}/{fname}{id}.jpg'

    def getOrigFilename(self, id: str):
        """Get the original photo filename from the id number."""
        return f'{self.dir}/_NZW{id}.JPG'
    
    def replaceAbbr(self, name: str):
        """Replace some common abbreviations."""
        key = name.strip()
        if key in self.dictAbbr:
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
    sp = SelectionParser('Nature-2024-01/Kandersteg.txt', 'Nature-2026-05/orig')
    result = sp.parse()
    for item in result:
        sp.log.info(item)

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)s %(name)s: %(message)s", 
        level=logging.DEBUG, handlers=[logging.StreamHandler()])
    testSelectionParser()
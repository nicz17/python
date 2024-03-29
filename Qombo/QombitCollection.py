"""
A collection of distinct qombits discovered by the player so far.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
from Qombit import *

class QombitCollection():
    log = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.qombits = set()

    def add(self, qombit: Qombit):
        """Add the qombit to the collection."""
        if qombit is not None:
            self.qombits.add(qombit)

    def getByKind(self, kind: OrKind):
        """Returns all qombits of the specified kind in this collection."""
        for qombit in self.qombits:
            if qombit.oKind == kind:
                yield qombit

    def clear(self):
        """Clears the collection."""
        self.qombits.clear()

    def toJson(self):
        """Export collection as JSON data."""
        data = []
        for qombit in self.qombits:
            data.append(qombit.toJson())
        return data

    def dump(self):
        """Dump collection contents to log."""
        self.log.info('Collection of %d qombits', len(self.qombits))
        for qombit in sorted(self.qombits):
            self.log.info('  %s', qombit)

    def __contains__(self, qombit: Qombit):
        return qombit in self.qombits
    
    def __len__(self):
        return len(self.qombits)
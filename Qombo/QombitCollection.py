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

    def dump(self):
        """Dump collection contents to log."""
        self.log.info('Collection of %d qombits', len(self.qombits))
        for qombit in sorted(self.qombits):
            self.log.info('  %s', qombit)

    def __contains__(self, qombit: Qombit):
        return qombit in self.qombits
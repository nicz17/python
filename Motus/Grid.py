"""
 A simple 2D grid containing objects in cells.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging

class Grid:
    """A simple 2D grid containing objects in cells."""
    log = logging.getLogger('Grid')

    def __init__(self, w: int, h: int):
        """Constructor with width and height."""
        self.w = w 
        self.h = h
        self.cells = [[None for i in range(h)] for j in range(w)]
        self.log.info('Constructed %s', self)

    def __str__(self):
        return 'Grid ' + str(self.w) + 'x' + str(self.h)
    
    def __repr__(self):
        return 'Grid(' + str(self.w) + ', ' + str(self.h) + ')'

    def __len__(self):
        """Returns the grid length (width x height)."""
        return self.w * self.h
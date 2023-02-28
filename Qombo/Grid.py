"""
 A 2D grid.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging

class Grid:
    log = logging.getLogger('Grid')

    """A simple 2D grid."""
    def __init__(self, w, h):
        """Constructor with width and height."""
        self.w = w 
        self.h = h
        self.cells = [[None for i in range(w)] for j in range(h)]
        self.log.info('Constructed %s', self.__str__())

    def put(self, x, y, val):
        self.cells[y][x] = val

    def size(self):
        """Returns the grid size (width x height)."""
        return self.w * self.h

    def dump(self):
        """Print internal state to log."""
        self.log.info('%s size %d', self.__str__(), self.size())
        self.log.info('%s', self.cells)

    def __str__(self):
        return 'Grid ' + str(self.w) + 'x' + str(self.h)

def testGrid():
    grid = Grid(5, 4)
    grid.put(0, 0, '0:0')
    grid.put(2, 3, '2:3')
    grid.put(4, 3, '4:3')
    grid.dump()
    
if __name__ == '__main__':
    logging.basicConfig(format="[%(levelname)s] %(message)s", 
        level=logging.DEBUG, handlers=[logging.StreamHandler()])
    testGrid()

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
        self.cells = [[None for i in range(h)] for j in range(w)]
        self.log.info('Constructed %s', self.__str__())

    def put(self, x, y, val):
        """Put the value in the x,y cell."""
        self.cells[x][y] = val

    def get(self, x, y):
        """Get the value in the x,y cell."""
        return self.cells[x][y]
    
    def isEmpty(self, x, y):
        """Checks if the x,y cell is empty."""
        return self.get(x, y) is None
    
    def clear(self):
        """Clears all cells."""
        for y in range(self.h):
            for x in range(self.w):
                self.put(x, y, None)

    def size(self):
        """Returns the grid size (width x height)."""
        return self.w * self.h
    
    def valueAsStr(self, x, y):
        """Get a string representation of the value at x,y."""
        if self.get(x, y):
            return str(self.get(x, y))
        return 'None'

    def dump(self):
        """Print internal state to log."""
        self.log.info('%s size %d', self.__str__(), self.size())
        for y in range(self.h):
            sRow = ''
            for x in range(self.w):
                sRow += self.valueAsStr(x, y).ljust(6)
            self.log.info(sRow)

    def __str__(self):
        return 'Grid ' + str(self.w) + 'x' + str(self.h)

def testGrid():
    grid = Grid(5, 4)
    grid.put(0, 0, '0:0')
    grid.put(1, 2, '1:2')
    grid.put(4, 3, '4:3')
    grid.dump()
    
if __name__ == '__main__':
    logging.basicConfig(format="[%(levelname)s] %(message)s", 
        level=logging.DEBUG, handlers=[logging.StreamHandler()])
    testGrid()

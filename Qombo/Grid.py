"""
 A simple 2D grid containing objects in cells.
 A 2D Position class for the grid coordinates.
 The grid is iterable; iteration yields positions.
"""

__author__ = "Nicolas Zwahlen"
__copyright__ = "Copyright 2023 N. Zwahlen"
__version__ = "1.0.0"

import logging
from math import sqrt

class Position:
    """A simple 2D position."""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def getDistance(self, pos):
        """Compute the distance to the specified position."""
        dx = self.x - pos.x
        dy = self.y - pos.y
        return sqrt(dx*dx + dy*dy)
    
    def __str__(self):
        return '[' + str(self.x) + ':' + str(self.y) + ']'
    
    def __repr__(self):
        return 'Position(' + str(self.x) + ', ' + str(self.y) + ')'
        
    def __eq__(self, other): 
        if not isinstance(other, Position):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.x == other.x and self.y == other.y

class Grid:
    """A simple 2D grid containing objects in cells."""
    log = logging.getLogger('Grid')

    def __init__(self, w: int, h: int):
        """Constructor with width and height."""
        self.w = w 
        self.h = h
        self.cells = [[None for i in range(h)] for j in range(w)]
        self.log.info('Constructed %s', self)

    def put(self, x: int, y: int, val):
        """Put the value in the x,y cell."""
        self.putAt(Position(x, y), val)

    def putAt(self, pos: Position, val):
        """Put the value in the specified cell."""
        if pos in self:
            self.cells[pos.x][pos.y] = val
        else:
            self.log.error('Invalid cell %s to put %s', pos, val)

    def get(self, x: int, y: int):
        """Get the value in the x,y cell."""
        return self.getAt(Position(x, y))
    
    def getAt(self, pos: Position):
        """Get the value at the specified position."""
        if pos in self:
            return self.cells[pos.x][pos.y]
        else:
            self.log.error('Invalid cell %s for get', pos)

    def find(self, val):
        """Return the location in this grid of the specified value, or None."""
        if val:
            for y in range(self.h):
                for x in range(self.w):
                    if self.get(x, y) == val:
                        return Position(x, y)
        return None
    
    def swap(self, pos1: Position, pos2: Position):
        """Swap the objects at pos1 and pos2"""
        self.log.info('Swapping %s and %s', pos1, pos2)
        obj1 = self.get(pos1.x, pos1.y)
        obj2 = self.get(pos2.x, pos2.y)
        self.put(pos1.x, pos1.y, obj2)
        self.put(pos2.x, pos2.y, obj1)
    
    def remove(self, val):
        """Removes the specified value, if it can be found. Returns removed object or None."""
        if val:
            for y in range(self.h):
                for x in range(self.w):
                    if self.get(x, y) == val:
                        self.log.info('Deleting at %d:%d %s', x, y, val)
                        self.put(x, y, None)
                        return val
        return None
    
    def isEmptyCell(self, x: int, y: int) -> bool:
        """Checks if the x,y cell is empty."""
        return self.get(x, y) is None
    
    def isFull(self) -> bool:
        """Checks if this grid is full."""
        for y in range(self.h):
            for x in range(self.w):
                if self.isEmptyCell(x, y):
                    return False
        return True
    
    def isEmpty(self) -> bool:
        """Checks if this grid is empty."""
        for y in range(self.h):
            for x in range(self.w):
                if not self.isEmptyCell(x, y):
                    return False
        return True
    
    def nextEmptyCell(self) -> Position:
        """Returns an empty cell position, or None if all full."""
        for y in range(self.h):
            for x in range(self.w):
                if self.isEmptyCell(x, y):
                    return Position(x, y)
        return None
    
    def closestEmptyCell(self, pos: Position) -> Position:
        """Return the closest empty cell to the sepcified position"""
        rMinDist = self.w + self.h
        closest = None
        for y in range(self.h):
            for x in range(self.w):
                if self.isEmptyCell(x, y):
                    rDist = pos.getDistance(Position(x, y))
                    if rDist < rMinDist:
                        rMinDist = rDist
                        closest = Position(x, y)
        return closest
    
    def getCenter(self) -> Position:
        """Returns the center of the grid"""
        return Position(int(self.w/2), int(self.h/2))
    
    def clear(self):
        """Clears all cells."""
        for y in range(self.h):
            for x in range(self.w):
                self.put(x, y, None)

    def size(self):
        """Returns the grid size (width x height)."""
        return self.w * self.h
    
    def count(self):
        """Counts non-empty cells."""
        iCount = 0
        for y in range(self.h):
            for x in range(self.w):
                if not self.isEmptyCell(x, y):
                    iCount += 1
        return iCount
    
    def valueAsStr(self, x, y):
        """Get a string representation of the value at x,y."""
        if self.get(x, y) is not None:
            return str(self.get(x, y))
        return 'None'

    def dump(self):
        """Print internal state to log."""
        self.log.info('%s size %d', self, self.size())
        for y in range(self.h):
            sRow = ''
            for x in range(self.w):
                sRow += self.valueAsStr(x, y).ljust(6)
            self.log.info(sRow)

    def toJson(self):
        """Create a dict of this grid for json export."""
        data = {}
        data['width']  = self.w
        data['height'] = self.h
        aCells = []
        for x in range(self.w):
            for y in range(self.h):
                val = self.get(x, y)
                if val is not None:
                    dCell = {}
                    dCell['x'] = x
                    dCell['y'] = y
                    opToJson = getattr(val, 'toJson', None)
                    if callable(opToJson):
                        dCell['value'] = val.toJson()
                    else:
                        dCell['value'] = val
                    aCells.append(dCell)
        data['cells'] = aCells
        return data

    def __str__(self):
        return 'Grid ' + str(self.w) + 'x' + str(self.h)
    
    def __repr__(self):
        return 'Grid(' + str(self.w) + ', ' + str(self.h) + ')'

    def __len__(self):
        """Returns the grid length (width x height)."""
        return self.w * self.h
    
    def __contains__(self, pos: Position):
        return pos.x >= 0 and pos.x < self.w and pos.y >= 0 and pos.y < self.h
    
    def __iter__(self):
        for x in range(self.w):
            for y in range(self.h):
                yield Position(x, y)

def testGrid():
    grid = Grid(5, 4)
    grid.log.info(repr(grid))
    grid.put(0, 0, '0:0')
    grid.put(1, 2, '1:2')
    grid.put(4, 3,  4.3)
    grid.put(4, 0,  4==0)
    grid.dump()
    grid.log.info('JSON: %s', grid.toJson())

    # Test iterable
    grid.log.info('Grid iteration:')
    for pos in grid:
        grid.log.info('.. %s', repr(pos))
    
if __name__ == '__main__':
    logging.basicConfig(format="[%(levelname)s] %(message)s", 
        level=logging.DEBUG, handlers=[logging.StreamHandler()])
    testGrid()

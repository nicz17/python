"""
Unit test for Grid class.
"""

import unittest
from Grid import *

class TestGrid(unittest.TestCase):

    def test_size(self):
        """Test grid size equals width x height."""
        grid = Grid(5, 4)
        self.assertEqual(grid.size(), 20, "Expected size 5x4")

    def test_count(self):
        """Test grid count equals number of not None cells."""
        grid = Grid(5, 4)
        self.assertEqual(grid.count(), 0, "Expected count empty")
        grid.put(0, 0, '0:0')
        grid.put(1, 2, '1:2')
        grid.put(4, 3, '4:3')
        self.assertEqual(grid.count(), 3, "Expected count after put 3")

    def test_empty(self):
        """Test grid empty check."""
        grid = Grid(5, 4)
        self.assertTrue(grid.isEmpty(), "Empty grid")
        grid.put(2, 3, True)
        self.assertFalse(grid.isEmpty(), "Non-empty grid")

    def test_json(self):
        """Test grid to JSON."""
        grid = Grid(5, 4)
        json = grid.toJson()
        self.assertIsNotNone(json, 'Json of empty grid')
        grid.put(2, 2, '2:2')
        json = grid.toJson()
        self.assertIsNotNone(json, 'Json of non-empty grid')

    def test_center(self):
        """Test grid center position."""
        grid = Grid(5, 5)
        center = grid.getCenter()
        self.assertEqual(center, Position(2, 2), 'Expected center at 2:2')

    def test_iterable(self):
        """Test that the grid is iterable."""
        nIterations = 0
        grid = Grid(5, 5)
        for pos in grid:
            self.assertIsNotNone(pos)
            nIterations += 1
        self.assertEqual(nIterations, 25, 'Expected 25 iteration positions')

if __name__ == '__main__':
    unittest.main()
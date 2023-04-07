"""
Unit test for Grid class.
"""

import unittest
from Grid import *

class TestPosition(unittest.TestCase):
    def test_distance(self):
        pos1 = Position(0, 0)
        pos2 = Position(3, 4)
        dist = pos1.getDistance(pos2)
        self.assertEqual(dist, 5.0, 'Expected distance 5.0')

    def test_equality(self):
        pos1 = Position(3, 3)
        pos2 = Position(2+1, 1+2)
        self.assertEqual(pos1, pos2, 'Expected Position(1+2, 2+1) == Position(3, 3)')

class TestGrid(unittest.TestCase):
    def test_size(self):
        """Test grid size equals width x height."""
        grid = Grid(5, 4)
        self.assertEqual(grid.size(), 20, "Expected size 5x4")

    def test_len(self):
        """Test grid length equals width x height."""
        grid = Grid(5, 4)
        self.assertEqual(len(grid), 20, "Expected length 5x4")

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

    def test_contains(self):
        """Test grid membership."""
        grid = Grid(5, 5)
        pos = Position(2, 2)
        self.assertTrue(pos in grid, 'Expected Position(2,2) in Grid(5,5)')
        pos = Position(4, 4)
        self.assertTrue(pos in grid, 'Expected Position(4,4) in Grid(5,5)')
        pos = Position(5, 4)
        self.assertFalse(pos in grid, 'Expected Position(5,4) not in Grid(5,5)')

    def test_outside(self):
        """Test putting objects in invalid cells."""
        grid = Grid(5, 4)
        grid.put(8, 12, 'No')
        grid.get(8, 12)
        pos = Position(7, 0)
        grid.putAt(pos, 'Nope')
        grid.getAt(pos)


if __name__ == '__main__':
    unittest.main()
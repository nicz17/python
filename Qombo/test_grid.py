"""
Unit test for Grid class.
"""

import unittest
from Grid import *

class TestGrid(unittest.TestCase):

    def test_size(self):
        grid = Grid(5, 4)
        self.assertEqual(grid.size(), 20, "Expected size 5x4")

    def test_count(self):
        grid = Grid(5, 4)
        self.assertEqual(grid.count(), 0, "Expected count empty")
        grid.put(0, 0, '0:0')
        grid.put(1, 2, '1:2')
        grid.put(4, 3, '4:3')
        self.assertEqual(grid.count(), 3, "Expected count after put 3")

    def test_empty(self):
        grid = Grid(5, 4)
        self.assertTrue(grid.isEmpty(), "Empty grid")
        grid.put(2, 3, True)
        self.assertFalse(grid.isEmpty(), "Non-empty grid")

    def test_json(self):
        grid = Grid(5, 4)
        json = grid.toJson()
        self.assertIsNotNone(json)
        grid.put(2, 2, '2:2')
        #json = grid.toJson()
        #self.assertIsNotNone(json)


if __name__ == '__main__':
    unittest.main()
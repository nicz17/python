"""
Unit test for HintProvider class.
"""

import unittest
from Grid import *
from HintProvider import *

class TestHint(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(5, 5)
        self.hintProv = HintProvider(grid)

    def test_empty(self):
        """Test hint on empty grid. Expect no hint."""
        hint = self.hintProv.getHint()
        self.assertIsNone(hint, 'Expected no hint')
        
    def test_gen(self):
        """Test hint with only one generator."""
        gen = QombitFactory.fromValues('Gen', OrKind.Generator, 1, OrRarity.Common)
        posGen = Position(0, 0)
        self.grid.putAt(posGen, gen)
        hint = self.hintProv.getHint()
        self.assertIsNotNone(hint, 'Expected a hint')
        for pos in hint:
            self.assertEquals(pos, posGen, 'Expected hint at (0,0)')
        
    def test_pair(self):
        """Test hint with a pair of qombits."""
        gen = QombitFactory.fromValues('Gen', OrKind.Generator, 1, OrRarity.Common)
        qombit = gen.generate()
        posGen = Position(0, 0)
        posQ1  = Position(1, 0)
        posQ2  = Position(2, 0)
        self.grid.putAt(posGen, gen)
        self.grid.putAt(posQ1, qombit)
        self.grid.putAt(posQ2, qombit)
        hint = self.hintProv.getHint()
        self.assertEquals(self.grid.count(), 3, 'Expected 3 qombits on grid')
        self.assertIsNotNone(hint, 'Expected a hint')
        for pos in hint:
            self.assertTrue(pos == posQ1 or pos == posQ2, 'Expected hint at (1,0) and (2,0)')


if __name__ == '__main__':
    unittest.main()

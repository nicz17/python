"""
Unit test for QombitCollection class.
"""

import unittest
from Qombit import *
from QombitFactory import *
from QombitCollection import *

class TestCollection(unittest.TestCase):
    """Unit test for QombitCollection class."""

    def setUp(self):
        #print('Running setup')
        self.collec = QombitCollection()
        self.star = QombitFactory.fromValues('Star', OrKind.Star, 1, OrRarity.Common)
        self.dice = QombitFactory.fromValues('Dice', OrKind.Dice, 1, OrRarity.Common)

    def test_distinct(self):
        """Test collection has no duplicates."""
        #print('Running distinct')
        self.assertEqual(len(self.collec), 0, 'Expected collection initially empty')
        self.assertFalse(self.star in self.collec, 'Expected star not in collection yet')
        self.collec.add(self.star)
        self.assertEqual(len(self.collec), 1, 'Expected collection size 1')
        self.assertTrue(self.star in self.collec, 'Expected qombit in collection now')
        self.collec.add(self.star)
        self.assertEqual(len(self.collec), 1, 'Expected collection size still 1')

    def test_evolve(self):
        """Test adding evolving qombits."""
        #print('Running evolve')
        iSize = 1
        nEvolutions = 5
        self.assertEqual(len(self.collec), 0, 'Expected collection initially empty')
        self.collec.add(self.star)
        self.assertEqual(len(self.collec), iSize, f'Expected collection size {iSize}')
        for iEvol in range(nEvolutions):
            self.star.evolve()
            iSize += 1
            self.collec.add(self.star)
            self.assertEqual(len(self.collec), iSize, f'Expected collection size {iSize}')

    def test_clear(self):
        """Test populating and clearing the collection."""
        self.assertEqual(len(self.collec), 0, 'Expected collection initially empty')
        self.collec.add(self.star)
        self.collec.add(self.dice)
        self.assertEqual(len(self.collec), 2, 'Expected collection size 2')
        self.collec.clear()
        self.assertEqual(len(self.collec), 0, 'Expected collection empty after clear')


if __name__ == '__main__':
    unittest.main()
